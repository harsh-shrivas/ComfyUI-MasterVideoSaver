================================================================================
REPOSITORY UPLOAD DETAILS
================================================================================
Repository Name: ComfyUI-MasterVideoSaver
Description    : Production-grade video export and canvas preview node for ComfyUI. Supports Apple ProRes 422 HQ (10-bit), H.264, WebM, and GIF with synchronized audio muxing.
Topics / Tags  : comfyui, comfyui-nodes, video-saver, prores-422-hq, ffmpeg, video-processing, vfx-pipeline, audio-muxing

Files to Upload:
├── __init__.py
├── master_video_saver.py
├── requirements.txt
└── README.md
(Do NOT upload desktop.ini or __pycache__)

================================================================================
requirements.txt
================================================================================
imageio
imageio-ffmpeg
soundfile
numpy
torch

================================================================================
README.md
================================================================================
# ComfyUI-MasterVideoSaver

A production-grade video export and real-time canvas preview node for ComfyUI.

Built for VFX compositors, video editors, and AI filmmakers who need mastering-grade outputs directly from ComfyUI workflows into Nuke, DaVinci Resolve, Premiere Pro, and After Effects. Eliminates washed-out colors and heavy compression artifacts by providing direct access to **10-bit Apple ProRes 422 HQ**, multi-format encoding, adjustable CRF quality controls, and frame-accurate synchronized audio muxing.

---

## Features

- **Apple ProRes 422 HQ (10-Bit):** Exports uncompressed mastering-grade footage (`prores_ks`, `yuv422p10le`) ready for professional grading and compositing timelines without color banding.
- **Multi-Codec Encoding Suite:** Choose between ProRes 422 HQ, H.264 (`.mp4` / `.mov`), VP9 (`.webm`), and animated `.gif` in a single node.
- **Synchronized Audio Muxing:** Route any upstream ComfyUI `AUDIO` connection directly into the node. Automatically encodes and muxes uncompressed PCM audio for `.mov` or AAC for `.mp4`/`.webm` without pitch shifts or sync drift.
- **Granular Quality Control (CRF):** Direct Constant Rate Factor (CRF 0–51) adjustment for fine-tuning compression efficiency and bitrate targets.
- **Arbitrary Directory Routing:** Output master renders directly to external fast scratch drives, NAS storage, or project directories (`Path\To\Destination\Folder`) with automatic fallback to ComfyUI's default output path.
- **In-Canvas Interactive Preview:** Generates a lightweight, browser-compatible preview stream directly on the node interface for immediate review upon queue completion.

---

## Installation

1. Navigate to your ComfyUI custom nodes directory:
   cd ComfyUI/custom_nodes

2. Clone this repository:
   git clone https://github.com/harsh-shrivas/ComfyUI-MasterVideoSaver.git

3. Install required dependencies:
   pip install imageio imageio-ffmpeg soundfile numpy torch

4. Restart ComfyUI.

---

## Usage

- **Category:** `Video Processing`
- **Node Name:** `Master Video Saver & Preview`
- **Workflow:**
  1. Route your image batch/latents decoded into the `images` pin.
  2. *(Optional)* Connect an `audio` pin from your voice generator or audio loader.
  3. Specify an absolute output folder in `export_directory` (e.g., `Path\To\Destination\Folder`). Leaving this blank defaults to `ComfyUI/output`.
  4. Set your filename prefix in `filename_prefix` (defaults to `Master_Video`).
  5. Select your target **FPS** and **Format** (e.g., `mov (prores - high quality)` or `mp4 (h264)`).
  6. Click **Queue Prompt**. Your master video will render to disk and populate the embedded video player on the canvas.

---

## Inputs & Outputs

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **images** | `IMAGE` (Input) | *Required* | Frame batch tensor (`[F, H, W, 3]`) |
| **export_directory** | `STRING` (Input) | `""` | Target directory for the exported file |
| **filename_prefix** | `STRING` (Input) | `""` | Output file base name |
| **fps** | `FLOAT` (Input) | `24.0` | Target frame rate (1.0 to 120.0 fps) |
| **format** | `COMBO` (Input) | `mov (prores - high quality)` | `mov (prores)`, `mov (h264)`, `mp4 (h264)`, `webm`, `gif` |
| **crf** | `INT` (Input) | `19` | Constant Rate Factor (0 for lossless, up to 51) |
| **audio** | `AUDIO` (Optional Input) | `None` | Audio dictionary (waveform + sample rate) for automated muxing |
| **filepath** | `STRING` (Output) | — | Absolute file path of the final rendered video |

---

## License

MIT License. Free to use, modify, and integrate into internal VFX pipelines and commercial production environments.
