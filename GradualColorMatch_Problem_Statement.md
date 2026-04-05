# GradualColorMatch — Problem Statement & Solution Plan

## Overview

In the `WanFirstLastFrameToVideo` workflow, the model generates video frames in its **own color style** throughout the entire video. The last generated frame does not match the color, contrast and lighting of the **source end image** (`#81 LoadImage`).

The source end image is darker, cooler and more desaturated — but the model generates a brighter, warmer, more saturated last frame.

---

## Problem Statement

### What is happening

| | Description |
|---|---|
| **Source end image (#81)** | Dark, cool, desaturated, moody |
| **Video last frame (-1)** | Bright, warm, saturated — model's own style |
| **Result** | Visible mismatch at the end of the video |

The model anchors the **composition** of the last frame to the source end image via `WanFirstLastFrameToVideo`, but it does **not** anchor the color, contrast or lighting. The model drifts to its own color style throughout generation and never returns to match the end image's look.

### Why ColorMatch does not work

The naive fix of inserting a `ColorMatch` node was attempted but failed because:

- `ColorMatch` locks the **entire video batch** to one reference frame's colors
- This destroys the natural color progression the model generates
- The result is a flat, unnatural look across all frames

---

## What We Actually Want

```
Frame 1:        100% model's natural color (matches start frame feel)
Frames 1–80:    model generates freely, natural progression untouched
Frames 80–120:  gradually shift colors toward end frame
Frame 121:      100% end frame colors matched
```

Not a hard snap. Not a full video color lock. A **gradual, smooth color transition** in the last portion of the video toward the end frame's color profile.

---

## Root Cause

`WanFirstLastFrameToVideo` anchors the **composition** of the last frame to the source end image, but does **not** anchor the color/contrast/lighting. The model drifts to its own internal color style and the last frame ends up visually inconsistent with the intended end image look.

---

## Solution Plan

### Build a custom ComfyUI node: `GradualColorMatch`

#### Inputs

| Input | Type | Description |
|---|---|---|
| `image_batch` | IMAGE | Full generated video batch from VAEDecode |
| `reference_image` | IMAGE | Source end image (#81) |
| `transition_start` | FLOAT | Where in the video the color shift begins (0.0–1.0) |

#### Logic Per Frame

```python
if frame_index < transition_start:
    weight = 0.0  # no color matching, frame untouched

else:
    weight = (frame_index - transition_start) / (1.0 - transition_start)
    weight = smoothstep(weight)  # smooth curve, not linear

blended_frame = lerp(original_frame, color_matched_frame, weight)
```

- `weight = 0.0` → original frame completely untouched
- `weight = 1.0` → frame fully color matched to end image
- `smoothstep` ensures a natural cinematic curve rather than a linear ramp

#### Output

- Modified image batch with the same number of frames
- Only the tail end of the video is affected
- Earlier frames are completely untouched

---

## Insert Point in Workflow

```
#72 VAEDecode (full batch output)
        ↓
GradualColorMatch        ← new custom node
  reference = #81        (source end image)
  transition_start = 0.7 (shift starts at 70% through video)
        ↓
#78 RIFE VFI
        ↓
VHS VideoCombine
```

---

## Exposed Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `transition_start` | float 0.0–1.0 | `0.7` | Where the color shift begins in the video |
| `transition_curve` | combo | `smoothstep` | `linear` / `smoothstep` / `ease-in` |
| `match_luminance` | boolean | `true` | Match brightness of end image |
| `match_contrast` | boolean | `true` | Match contrast of end image |
| `match_color` | boolean | `false` | Match hue and saturation of end image |

> **Note:** `match_color` is off by default to preserve the model's natural color palette. Only brightness and contrast are corrected by default, which is the core of the problem.

---

## Workflow Nodes Reference (Antigravity_new_node_build)

| Node ID | Type | Role |
|---|---|---|
| `#25` | LoadImage | Start frame source |
| `#81` | LoadImage | End frame source |
| `#37` | LayerUtility: ImageScaleByAspectRatio | Scales start frame |
| `#40` | LayerUtility: ImageScaleByAspectRatio | Scales end frame |
| `#70` | WanFirstLastFrameToVideo | Core generation node |
| `#52` / `#46` | KSamplerAdvanced | High / low noise samplers |
| `#72` | VAEDecode | Decodes latent batch to images |
| `#74` / `#77` | GetImagesFromBatchIndexed | Previews first and last frames |
| `#75` | Image Comparer | Compares start vs end frame |
| `#78` | RIFE VFI | Frame interpolation (×2) |
| `#82` | PreviewImage | Final last frame preview |

---

## Next Step

Write the Python code for the `GradualColorMatch` custom node.
