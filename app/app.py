"""Z-Image-Turbo - Complete Image Generation App.

Uses the local z_image_turbo_bf16.safetensors model file.
"""

import os
import sys
import time
import threading
import queue
from pathlib import Path

# Add the app directory to path
APP_DIR = Path(__file__).parent
sys.path.insert(0, str(APP_DIR))

# Model configuration
MODEL_PATH = os.environ.get(
    "Z_IMAGE_MODEL_PATH",
    r"I:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\z_image_turbo_bf16.safetensors"
)

# Try to find the model in common locations
def find_model():
    """Find the Z-Image-Turbo model file."""
    candidates = [
        MODEL_PATH,
        r"I:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\z_image_turbo_bf16.safetensors",
        r"E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\z_image_turbo_bf16.safetensors",
        r"I:\ComfyUI_windows_portable\ComfyUI\models\checkpoints\z_image_turbo.safetensors",
        r"E:\ComfyUI_windows_portable\ComfyUI\models\checkpoints\z_image_turbo.safetensors",
        r"I:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\cyberrealisticZImage_v30.safetensors",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def generate_image(
    prompt: str,
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    num_inference_steps: int = 8,
    guidance_scale: float = 0.0,
    seed: int = 0,
):
    """Generate an image from a text prompt."""
    import torch
    from diffusers import StableDiffusionPipeline
    
    model_path = find_model()
    if not model_path:
        raise FileNotFoundError("Z-Image-Turbo model not found. Please check the model path.")
    
    print(f"Loading model from: {model_path}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    
    # Load the model
    pipe = StableDiffusionPipeline.from_single_file(
        model_path,
        torch_dtype=dtype,
        safety_checker=None,
        requires_safety_checker=False,
    )
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()
    
    if hasattr(pipe, "enable_vae_slicing"):
        pipe.enable_vae_slicing()
    
    # Generate
    if seed == 0:
        seed = torch.randint(0, 2**32, (1,)).item()
    
    generator = torch.Generator(device=device).manual_seed(seed)
    
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator,
    )
    
    image = result.images[0]
    return image, seed


def create_app():
    """Create the Gradio interface."""
    import gradio as gr
    
    with gr.Blocks(title="Z-Image-Turbo") as demo:
        gr.Markdown("# ⚡ Z-Image-Turbo")
        gr.Markdown("Fast image generation with the Z-Image-Turbo model (6B parameters, sub-second inference)")
        
        with gr.Row():
            with gr.Column(scale=1):
                prompt = gr.Textbox(
                    label="Prompt",
                    placeholder="A majestic dragon at sunset",
                    lines=3,
                )
                negative_prompt = gr.Textbox(
                    label="Negative Prompt",
                    placeholder="",
                    lines=2,
                )
                with gr.Row():
                    width = gr.Slider(
                        label="Width",
                        minimum=256,
                        maximum=2048,
                        step=64,
                        value=1024,
                    )
                    height = gr.Slider(
                        label="Height",
                        minimum=256,
                        maximum=2048,
                        step=64,
                        value=1024,
                    )
                with gr.Row():
                    steps = gr.Slider(
                        label="Steps",
                        minimum=1,
                        maximum=50,
                        step=1,
                        value=8,
                    )
                    guidance = gr.Slider(
                        label="Guidance Scale",
                        minimum=0.0,
                        maximum=20.0,
                        step=0.5,
                        value=0.0,
                    )
                seed = gr.Number(
                    label="Seed (0 for random)",
                    value=0,
                    precision=0,
                )
                generate_btn = gr.Button("Generate", variant="primary", size="lg")
            
            with gr.Column(scale=1):
                output_image = gr.Image(label="Generated Image", type="pil")
                output_seed = gr.Number(label="Seed Used", precision=0)
        
        def on_generate(prompt, negative_prompt, width, height, steps, guidance, seed):
            image, used_seed = generate_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=int(width),
                height=int(height),
                num_inference_steps=int(steps),
                guidance_scale=float(guidance),
                seed=int(seed),
            )
            return image, used_seed
        
        generate_btn.click(
            fn=on_generate,
            inputs=[prompt, negative_prompt, width, height, steps, guidance, seed],
            outputs=[output_image, output_seed],
        )
    
    return demo


if __name__ == "__main__":
    print("=== Z-Image-Turbo ===")
    print(f"Model path: {MODEL_PATH}")
    print(f"Model exists: {os.path.exists(MODEL_PATH)}")
    
    # Find the actual model
    actual_model = find_model()
    if actual_model:
        print(f"Found model: {actual_model}")
        sz = os.path.getsize(actual_model) / (1024**3)
        print(f"Model size: {sz:.2f} GB")
    else:
        print("WARNING: No model file found!")
        print("Please set Z_IMAGE_MODEL_PATH environment variable.")
        sys.exit(1)
    
    # Create and launch the app
    demo = create_app()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
    )
