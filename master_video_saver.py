import os
import random
import subprocess
import numpy as np
import torch
import imageio
import folder_paths

class MasterVideoSaver:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "export_directory": ("STRING", {"default": ""}),
                "filename_prefix": ("STRING", {"default": ""}),
                "fps": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 120.0, "step": 1.0}),
                "format": ([
                    "mov (prores - high quality)", 
                    "mov (h264)", 
                    "mp4 (h264)", 
                    "webm", 
                    "gif"
                ], {"default": "mov (prores - high quality)"}),
                "crf": ("INT", {"default": 19, "min": 0, "max": 51, "step": 1}),
            },
            "optional": {
                "audio": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filepath",)
    FUNCTION = "process_video"
    OUTPUT_NODE = True
    CATEGORY = "Video Processing"

    def process_video(self, images, export_directory, filename_prefix, fps, format, crf, audio=None):
        target_dir = export_directory.strip() if export_directory.strip() else self.output_dir
        target_prefix = filename_prefix.strip() if filename_prefix.strip() else "Master_Video"
        os.makedirs(target_dir, exist_ok=True)

        if "mov" in format:
            ext = "mov"
        elif "webm" in format:
            ext = "webm"
        elif "gif" in format:
            ext = "gif"
        else:
            ext = "mp4"

        full_custom_path = os.path.join(target_dir, f"{target_prefix}.{ext}")

        # Convert IMAGE tensor [F, H, W, 3] (0.0 - 1.0) to uint8 numpy array
        frames_np = (images.cpu().numpy() * 255).clip(0, 255).astype(np.uint8)

        # Configure Codec & Pixel Format
        if ext == "gif":
            imageio.mimsave(full_custom_path, frames_np, fps=fps)
        else:
            if "prores" in format:
                codec = "prores_ks"
                pix_fmt = "yuv422p10le"
                output_params = ["-profile:v", "3"]  # ProRes 422 HQ
            elif ext == "webm":
                codec = "libvpx-vp9"
                pix_fmt = "yuv420p"
                output_params = ["-crf", str(crf)]
            else:
                codec = "libx264"
                pix_fmt = "yuv420p"
                output_params = ["-crf", str(crf)]

            writer = imageio.get_writer(
                full_custom_path,
                fps=fps,
                codec=codec,
                pixelformat=pix_fmt,
                output_params=output_params
            )
            for frame in frames_np:
                writer.append_data(frame)
            writer.close()

            # Mux Audio if connected
            if audio is not None and ext in ["mp4", "mov", "webm"]:
                try:
                    import soundfile as sf
                    temp_audio_path = os.path.join(folder_paths.get_temp_directory(), f"temp_audio_{random.randint(1000,9999)}.wav")
                    waveform = audio["waveform"]
                    sr = audio["sample_rate"]
                    if waveform.ndim == 3:
                        waveform = waveform.squeeze(0)
                    sf.write(temp_audio_path, waveform.cpu().numpy().T, sr, subtype="PCM_16")

                    import imageio_ffmpeg
                    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                    temp_muxed_path = os.path.join(target_dir, f"{target_prefix}_temp.{ext}")

                    cmd = [
                        ffmpeg_exe, "-y",
                        "-i", full_custom_path,
                        "-i", temp_audio_path,
                        "-c:v", "copy",
                        "-c:a", "pcm_s16le" if ext == "mov" else "aac",
                        "-shortest",
                        temp_muxed_path
                    ]
                    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    os.replace(temp_muxed_path, full_custom_path)
                    if os.path.exists(temp_audio_path):
                        os.remove(temp_audio_path)
                except Exception as e:
                    print(f"[MasterVideoSaver] Audio muxing notice: {e}")

        # Temp preview for UI player
        temp_dir = folder_paths.get_temp_directory()
        preview_file = f"preview_{random.randint(100000, 999999)}.mp4"
        preview_path = os.path.join(temp_dir, preview_file)
        
        # Save browser-compatible MP4 preview for node canvas view
        writer = imageio.get_writer(preview_path, fps=fps, codec='libx264', pixelformat='yuv420p')
        for frame in frames_np:
            writer.append_data(frame)
        writer.close()

        return {
            "ui": {
                "gifs": [{
                    "filename": preview_file,
                    "type": "temp",
                    "subfolder": ""
                }]
            },
            "result": (full_custom_path,)
        }

NODE_CLASS_MAPPINGS = {"MasterVideoSaver": MasterVideoSaver}
NODE_DISPLAY_NAME_MAPPINGS = {"MasterVideoSaver": "Master Video Saver & Preview"}
