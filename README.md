# Z-Image-Turbo for Pinokio

⚡️ Z-Image-Turbo - Efficient 6B parameter image generation model with sub-second inference, packaged for Pinokio.

A Gradio web interface for the Z-Image-Turbo model, designed for easy installation via [Pinokio](https://pinokio.computer/).

## Features

- **One-Click Install** - Pinokio handles all dependencies automatically
- **Modern Gradio UI** - Clean interface with all generation options
- **High-Quality Images** - Uses the Z-Image-Turbo model from Tongyi-MAI
- **Fast Generation** - Turbo model generates images in just 8 steps
- **Full Control** - Adjustable dimensions, steps, guidance, and seed

## Installation

### Via Pinokio (Recommended)

1. Install [Pinokio](https://pinokio.computer/)
2. Search for "Z-Image-Turbo" or add this repository URL
3. Click **Install** - Pinokio will:
   - Create a Python virtual environment
   - Install PyTorch with CUDA support
   - Install all Python dependencies
   - Download the Z-Image-Turbo model
4. Click **Start** to launch the app
5. Use **Reset** to delete the virtual environment if you want a fresh reinstall
6. Use **Update** to pull the latest changes from git

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/PierrunoYT/Z-Image-Pinokio.git
cd Z-Image-Pinokio

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt

# Run the app
python app/app.py
```

## Usage

### Web UI

Once started, open the Gradio interface in your browser:

- **Prompt**: Describe the image you want to generate
- **Negative Prompt**: Describe what you don't want in the image
- **Width/Height**: Image dimensions (256-2048)
- **Steps**: Number of inference steps (1-50, default 8)
- **Guidance Scale**: How closely to follow the prompt (0-20, default 0)
- **Seed**: Random seed (0 for random)

### HTTP API

The app exposes a REST API at `http://127.0.0.1:7860/run/generate`:

```bash
curl -X POST "http://127.0.0.1:7860/run/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      "A majestic dragon at sunset",
      "",
      1024,
      1024,
      8,
      0.0,
      42
    ]
  }'
```

### Python

```python
from gradio_client import Client

client = Client("http://127.0.0.1:7860")
result = client.predict(
    prompt="A majestic dragon at sunset",
    negative_prompt="",
    width=1024,
    height=1024,
    num_inference_steps=8,
    guidance_scale=0.0,
    seed=42,
    randomize_seed=False,
    api_name="/predict",
)
print(result)  # (filepath, seed_used)
```

## Model Info

- **Model**: [Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)
- **License**: Apache 2.0
- **Size**: ~12GB

## Credits

- **Z-Image-Turbo**: [Tongyi-MAI (Alibaba)](https://huggingface.co/Tongyi-MAI)
- **Diffusers**: [Hugging Face](https://github.com/huggingface/diffusers)
- **Pinokio**: [Pinokio](https://pinokio.computer/)

## License

MIT
