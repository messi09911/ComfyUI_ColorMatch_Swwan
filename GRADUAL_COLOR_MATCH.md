# Gradual Color Match (Swwan)

A custom ComfyUI node that fixes the **color-drift problem** in `WanFirstLastFrameToVideo` workflows.

---

## The Problem

When using `WanFirstLastFrameToVideo`, the model anchors the **composition** of the last frame to a source end image — but it does **not** anchor the color, contrast, or lighting. The model drifts to its own internal color style throughout generation, causing a visible mismatch at the end of the video.

| | Description |
|---|---|
| **Source end image** | Dark, cool, desaturated, moody |
| **Generated last frame** | Bright, warm, saturated — model's own style |
| **Result** | Visible color mismatch at the end |

The naive fix (inserting a standard `Color Match` node) fails because it locks the **entire video batch** to one reference color — destroying the natural progression the model generates and resulting in a flat, unnatural look.

---

## The Solution

`Gradual Color Match (Swwan)` applies color matching **only to the tail** of the video, using a smooth blend curve:

```
Frame 0        →  100% model's natural color (untouched)
Frames 0–70%   →  model generates freely, completely untouched
Frames 70–100% →  smoothly blend colors toward reference end image
Frame 100%     →  100% color-matched to reference
```

---

## Workflow Position

Insert the node between `VAEDecode` and `RIFE VFI`:

```
#72 VAEDecode
      ↓
Gradual Color Match (Swwan)   ← NEW
  image_batch   = output of #72
  reference_image = #81 LoadImage (your end frame)
  transition_start = 0.7
      ↓
#78 RIFE VFI
      ↓
VHS VideoCombine
```

---

## Inputs

### Required

| Input | Type | Description |
|---|---|---|
| `image_batch` | IMAGE | Full video batch from VAEDecode |
| `reference_image` | IMAGE | Source end image (your target color look) |
| `transition_start` | FLOAT `0.0–1.0` | Where in the video color blending begins. `0.7` = last 30% of frames affected |

### Optional

| Input | Type | Default | Description |
|---|---|---|---|
| `method` | combo | `mkl` | Color transfer algorithm (see below) |
| `transition_curve` | combo | `smoothstep` | Blend curve shape (see below) |
| `max_strength` | FLOAT `0.0–1.0` | `1.0` | Blend weight at the very last frame |
| `multithread` | BOOLEAN | `true` | Process frames in parallel for speed |

---

## Options Reference

### `method` — Color Transfer Algorithm

| Value | Description |
|---|---|
| `mkl` | Monge-Kantorovich Linearization — best overall quality ✅ recommended |
| `hm` | Histogram Matching — fast, channel-by-channel |
| `reinhard` | Classic Reinhard LAB-space transfer — good for natural looks |
| `mvgd` | Multi-Variate Gaussian Distribution — mathematically precise |
| `hm-mvgd-hm` | Compound HM→MVGD→HM — highest quality, slower |
| `hm-mkl-hm` | Compound HM→MKL→HM — very high quality |

Powered by [`color-matcher`](https://github.com/hahnec/color-matcher) by Reinhard et al. / Pitie et al.

---

### `transition_start` — How it works

The node normalises every frame index to `0.0 → 1.0` based on the total batch size — so `0.7` **always** means "start at 70% through whatever video I receive", regardless of frame count.

**Example — 121-frame video:**

| Frame | Normalised | Effect |
|---|---|---|
| 0–83 | 0.00 – 0.69 | ❌ Untouched — model's original color |
| 84 | 0.70 | ✅ Blending begins |
| 96 | 0.80 | ✅ ~50% blended |
| 108 | 0.90 | ✅ ~75% blended |
| 120 | 1.00 | ✅ `max_strength` % blended |

---

### `transition_curve` — Blend Curve Shape

| Value | Feel |
|---|---|
| `smoothstep` | Slow start, fast middle, slow end — most cinematic ✅ |
| `linear` | Constant ramp |
| `ease_in` | Slow start, accelerates — subtle then sudden |
| `ease_out` | Fast start, decelerates — hits quickly then settles |

---

### `max_strength`

Controls how strongly the color match is applied at the very last frame.  
- `1.0` → last frame is 100% matched to the reference  
- `0.8` → last frame retains 20% of the model's original color  
- `0.0` → effectively disables the node  

---

## Recommended Settings

| Parameter | Value |
|---|---|
| `transition_start` | `0.70` |
| `method` | `mkl` |
| `transition_curve` | `smoothstep` |
| `max_strength` | `1.0` |
| `multithread` | `true` |

**Tuning tips:**
- If the last frame still looks too strong → lower `max_strength` to `0.85`
- If the transition feels too abrupt → lower `transition_start` to `0.60` so it blends over more frames
- For the highest quality result (slower) → switch `method` to `hm-mvgd-hm`

---

## Output

| Output | Type | Description |
|---|---|---|
| `image` | IMAGE | Same batch size as input — early frames bit-for-bit identical, tail frames gradually color-corrected |

---

## Requirements

```
color-matcher
```

Install with:
```bash
pip install color-matcher
```

This is the same dependency used by the existing `Color Match (Swwan)` node — if that node already works in your ComfyUI setup, no additional installation is required.

---

## File

**`gradual_color_match.py`** — self-contained, no external scripts required.  
Registered under category `Swwan/Video`.

---

## Credits

- Color transfer algorithms: [`color-matcher`](https://github.com/hahnec/color-matcher) by hahnec
- Original node collection: [ComfyUI_Swwan](https://github.com/aining2022/ComfyUI_Swwan) by aining2022
- Part of **Color Match Swwan Update**
