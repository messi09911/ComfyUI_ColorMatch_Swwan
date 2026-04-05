import torch
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import os


def _smoothstep(t):
    """Smooth hermite curve: 3t² - 2t³"""
    return t * t * (3.0 - 2.0 * t)


def _ease_in(t):
    """Quadratic ease-in: t²"""
    return t * t


def _ease_out(t):
    """Quadratic ease-out: 1 - (1-t)²"""
    return 1.0 - (1.0 - t) * (1.0 - t)


def _linear(t):
    return t


CURVE_FNS = {
    "smoothstep": _smoothstep,
    "linear":     _linear,
    "ease_in":    _ease_in,
    "ease_out":   _ease_out,
}


class GradualColorMatch:
    """
    Gradually blends color-matching toward a reference image over the tail of a
    video batch.  Early frames are completely untouched; only the last portion
    (beyond transition_start) is shifted — smoothly — toward the reference look.

    Designed to fix the color-drift problem in WanFirstLastFrameToVideo workflows:
        #72 VAEDecode → GradualColorMatch → #78 RIFE VFI
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_batch": ("IMAGE",),
                "reference_image": ("IMAGE",),
                "transition_start": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": (
                        "Normalised frame index where color blending begins. "
                        "0.7 = shift starts at 70% through the video."
                    ),
                }),
            },
            "optional": {
                "method": (
                    ["mkl", "hm", "reinhard", "mvgd", "hm-mvgd-hm", "hm-mkl-hm"],
                    {"default": "mkl"},
                ),
                "transition_curve": (
                    ["smoothstep", "linear", "ease_in", "ease_out"],
                    {"default": "smoothstep"},
                ),
                "max_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": (
                        "Maximum blend weight at the very last frame. "
                        "1.0 = fully color-matched on the last frame."
                    ),
                }),
                "multithread": ("BOOLEAN", {"default": True}),
            },
        }

    CATEGORY = "Swwan/Video"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply"
    DESCRIPTION = """\
GradualColorMatch — fixes the color-drift problem in WanFirstLastFrameToVideo.

Early frames are untouched. Starting at `transition_start` (e.g. 0.7 = 70% through
the video), frames are progressively blended toward the reference image's color
profile using the same MKL / HM / Reinhard methods as Color Match (Swwan).

Insert between VAEDecode (#72) and RIFE VFI (#78):
    VAEDecode → GradualColorMatch (ref = end LoadImage) → RIFE VFI
"""

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _weight_for_frame(frame_idx, total_frames, transition_start, curve_fn):
        """Return blend weight [0, 1] for a given frame index."""
        if total_frames <= 1:
            return 1.0
        t_norm = frame_idx / (total_frames - 1)          # 0 … 1
        if t_norm < transition_start:
            return 0.0
        span = 1.0 - transition_start
        if span <= 0.0:
            return 1.0
        t = (t_norm - transition_start) / span            # 0 … 1 within tail
        t = max(0.0, min(1.0, t))
        return curve_fn(t)

    @staticmethod
    def _color_match_single(src_np, ref_np, method, cm):
        """Apply color transfer and return float32 numpy array clipped to [0,1]."""
        try:
            result = cm.transfer(src=src_np, ref=ref_np, method=method)
            return np.clip(result, 0.0, 1.0).astype(np.float32)
        except Exception as e:
            print(f"[GradualColorMatch] color_matcher error: {e}")
            return src_np.astype(np.float32)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def apply(
        self,
        image_batch,
        reference_image,
        transition_start=0.7,
        method="mkl",
        transition_curve="smoothstep",
        max_strength=1.0,
        multithread=True,
    ):
        try:
            from color_matcher import ColorMatcher
        except ImportError:
            raise ImportError(
                "[GradualColorMatch] Cannot import color-matcher. "
                "Install it with: pip install color-matcher"
            )

        curve_fn = CURVE_FNS.get(transition_curve, _smoothstep)

        # Move everything to CPU (color-matcher works on numpy arrays)
        batch = image_batch.cpu()           # (B, H, W, C)  float32  0..1
        ref   = reference_image.cpu()       # (1+, H, W, C)

        B = batch.shape[0]

        ref_np = ref[0].numpy()             # always use first ref frame

        # Pre-compute weights so we can skip frames with weight == 0
        weights = [
            self._weight_for_frame(i, B, transition_start, curve_fn) * max_strength
            for i in range(B)
        ]

        # Identify which frames actually need processing
        active = [i for i, w in enumerate(weights) if w > 0.0]

        if not active:
            # Nothing to do — all frames before transition_start
            return (image_batch.clone(),)

        def process_frame(i):
            w = weights[i]
            src_np = batch[i].numpy()          # (H, W, C) float32
            cm = ColorMatcher()
            matched_np = self._color_match_single(src_np, ref_np, method, cm)
            # Lerp: original + weight * (matched - original)
            blended = src_np + w * (matched_np - src_np)
            return i, np.clip(blended, 0.0, 1.0).astype(np.float32)

        # Build output tensor (start as a copy so untouched frames are already correct)
        out_np = batch.numpy().copy()          # (B, H, W, C )

        if multithread and len(active) > 1:
            max_threads = min(os.cpu_count() or 1, len(active))
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = {executor.submit(process_frame, i): i for i in active}
                for future in futures:
                    idx, blended = future.result()
                    out_np[idx] = blended
        else:
            for i in active:
                _, blended = process_frame(i)
                out_np[i] = blended

        out = torch.from_numpy(out_np).to(torch.float32)
        out.clamp_(0.0, 1.0)
        return (out,)


# ------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "GradualColorMatch": GradualColorMatch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GradualColorMatch": "Gradual Color Match (Swwan)",
}
