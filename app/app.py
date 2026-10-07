"""Z-Image-Turbo Gradio App.

Uses the Tongyi-MAI/Z-Image-Turbo model via Diffusers for fast image generation.
"""

import os
import torch
from diffusers import StableDiffusionPipeline

# Model ID from Hugging Face
MODEL_ID = "Tongyi-MAI/Z-Image-Turbo"

# Local model path (if downloaded)
LOCAL_MODEL_PATH = os.environ.get("Z_IMAGE_MODEL_PATH", None)

# Device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# Load model
if LOCAL_MODEL_PATH and os.path.isdir(LOCAL_MODEL_PATH):
    print(f"Loading model from local path: {LOCAL_MODEL_PATH}")
    pipe = StableDiffusionPipeline.from_pretrained(
        LOCAL_MODEL_PATH,
        torch_dtype=DTYPE,
        safety_checker=None,
        requires_safety_checker=False,
    )
else:
    print(f"Loading model from Hugging Face: {MODEL_ID}")
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=DTYPE,
        safety_checker=None,
        requires_safety_checker=False,
    )

pipe = pipe.to(DEVICE)
pipe.enable_attention_slicing()

# Enable memory efficient attention if available
if hasattr(pipe, "enable_vae_slicing"):
    pipe.enable_vae_slicing()


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
    if seed == 0:
        seed = torch.randint(0, 2**32, (1,)).item()

    generator = torch.Generator(device=DEVICE).manual_seed(seed)

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


def create_demo():
    """Create the Gradio interface."""
    import gradio as gr

    with gr.Blocks(title="Z-Image-Turbo", theme=gr.themes.Soft()) as demo:
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

        # API endpoint
        api = gr.Interface(
            fn=generate_image,
            inputs=[
                gr.Textbox(label="Prompt"),
                gr.Textbox(label="Negative Prompt"),
                gr.Slider(label="Width", minimum=256, maximum=2048, step=64, value=1024),
                gr.Slider(label="Height", minimum=256, maximum=2048, step=64, value=1024),
                gr.Slider(label="Steps", minimum=1, maximum=50, step=1, value=8),
                gr.Slider(label="Guidance Scale", minimum=0.0, maximum=20.0, step=0.5, value=0.0),
                gr.Number(label="Seed", value=0, precision=0),
            ],
            outputs=[gr.Image(label="Image"), gr.Number(label="Seed")],
            api_name="generate",
        )

    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
    )
