# Color Match Swwan Update

> A focused update to [ComfyUI_Swwan](https://github.com/aining2022/ComfyUI_Swwan) by aining2022 — adding the `Gradual Color Match` node to solve the end-frame color drift problem in `WanFirstLastFrameToVideo` workflows.

---

## What's New

### 🎨 Gradual Color Match (Swwan)

The core addition of this update. Fixes the color-drift problem where `WanFirstLastFrameToVideo` generates a last frame that is brighter, warmer, and more saturated than the intended source end image.

**Unlike a standard Color Match node**, this node:
- Leaves early frames **completely untouched** ✅
- Applies color blending **only to the tail** of the video ✅
- Uses a **smooth curve** (smoothstep / ease-in / ease-out / linear) for a cinematic feel ✅

→ **[Full documentation: GRADUAL_COLOR_MATCH.md](GRADUAL_COLOR_MATCH.md)**

---

## Workflow Position

```
#72 VAEDecode
      ↓
Gradual Color Match (Swwan)
  image_batch    = output of #72 (VAEDecode)
  reference_image = #81 (LoadImage — your end frame)
  transition_start = 0.7
      ↓
#78 RIFE VFI
      ↓
VHS VideoCombine
```

Find the node in ComfyUI under: **`Swwan/Video → Gradual Color Match (Swwan)`**

---

## All Nodes

This pack includes the full ComfyUI_Swwan node collection plus the new Gradual Color Match node.

### Image Processing

| Node | Description |
|------|-------------|
| Image Resize KJ v2 | Multi-mode image resize with crop/pad/stretch |
| Image Resize By Megapixels | Resize by target megapixels with aspect ratio control |
| Image Concatenate | Concatenate images (horizontal/vertical) |
| Image Concat From Batch | Concatenate images from batch |
| Image Grid Composite 2x2/3x3 | 2x2/3x3 grid composition |
| Color Match | Color matching (MKL, HM, Reinhard, MVGD) |
| **Gradual Color Match** | **Gradual tail-only color matching — [docs](GRADUAL_COLOR_MATCH.md)** |
| Save Image With Alpha | Save image with alpha channel |
| Cross Fade Images | Image cross-fade transition |
| Add Label | Add text label to image |
| Image Pad KJ | Image padding |
| Draw Mask On Image | Draw mask overlay on image |

### Image Cropping

| Node | Description |
|------|-------------|
| CropByMask V2/V3/V4/V5 | Smart mask-based cropping |
| RestoreCropBox V1–V4 | Restore cropped area to original |
| Image Crop By Mask | Crop by mask |
| Image Crop By Mask And Resize | Crop and resize |
| Image Uncrop By Mask | Restore crop |

### Batch Operations

| Node | Description |
|------|-------------|
| Get Image Range From Batch | Get image range from batch |
| Get Images From Batch Indexed | Get images by index |
| Insert Images To Batch Indexed | Insert images by index |
| Replace Images In Batch | Replace images in batch |
| Shuffle Image Batch | Shuffle image order |
| Reverse Image Batch | Reverse image order |
| Image Batch Multi | Multi-image batch merge |
| Image List To Batch / Batch To List | List-batch conversion |

### Scaling

| Node | Description |
|------|-------------|
| ImageScaleByAspectRatio V2 | Scale by aspect ratio |
| Image Resize Sum | Comprehensive resize node |
| Load And Resize Image | Load and resize image |

### Mask Processing

| Node | Description |
|------|-------------|
| Mask Transform Sum | Mask transformation |
| NSFW Detector V2 | NSFW content detection |

### Math

| Node | Description |
|------|-------------|
| Math Expression | Math expression evaluation |
| Math Calculate | Math calculation |
| Math Remap Data | Value remapping |
| C Math | Extended math nodes |

### Switch & Control

| Node | Description |
|------|-------------|
| Any Switch | Any type switch |

### Utility

| Node | Description |
|------|-------------|
| Seed | Seed node (random/increment) |
| Get Image Size & Count | Get image size and count |
| Get Latent Size & Count | Get latent size and count |
| Preview Animation | Animation preview |
| Fast Preview | Fast preview |
| IO Nodes | Input/Output utility nodes |

---

## Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_USERNAME/ComfyUI_ColorMatch_Swwan
pip install -r ComfyUI_ColorMatch_Swwan/requirements.txt
```

> **Note:** `Gradual Color Match` requires the `color-matcher` library — already included in `requirements.txt`. If your existing `Color Match (Swwan)` node works, no extra installation is needed.

---

## Requirements

```
color-matcher
```

---

## Credits

- **[ComfyUI_Swwan](https://github.com/aining2022/ComfyUI_Swwan)** by aining2022 — original node collection this is based on
- **[ComfyUI_LayerStyle](https://github.com/chflame163/ComfyUI_LayerStyle)** by chflame163 — upstream source for several nodes
- **[ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes)** by kijai — upstream source for several nodes
- **[rgthree-comfy](https://github.com/rgthree/rgthree-comfy)** by rgthree
- **[color-matcher](https://github.com/hahnec/color-matcher)** by hahnec — color transfer algorithms (MKL, HM, Reinhard, MVGD)
