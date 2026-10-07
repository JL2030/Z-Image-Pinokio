// Z-Image-Turbo Install Script for Pinokio
// Installs dependencies and downloads the model

const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const APP_PATH = __dirname;
const ENV_PATH = path.join(APP_PATH, 'env');

console.log('=== Z-Image-Turbo Install ===');

// Create virtual environment
if (!fs.existsSync(ENV_PATH)) {
  console.log('Creating virtual environment...');
  execSync(`python -m venv "${ENV_PATH}"`, { stdio: 'inherit' });
}

// Get python path
const pythonPath = path.join(ENV_PATH, 'Scripts', 'python.exe');
const pipPath = path.join(ENV_PATH, 'Scripts', 'pip.exe');

// Install PyTorch with CUDA
console.log('Installing PyTorch with CUDA support...');
execSync(`"${pipPath}" install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`, { stdio: 'inherit' });

// Install other dependencies
console.log('Installing Python dependencies...');
execSync(`"${pipPath}" install -r "${path.join(APP_PATH, 'app', 'requirements.txt')}"`, { stdio: 'inherit' });

// Download model
console.log('Downloading Z-Image-Turbo model...');
execSync(`"${pythonPath}" -c "from huggingface_hub import snapshot_download; snapshot_download('Tongyi-MAI/Z-Image-Turbo', local_dir='${path.join(APP_PATH, 'model')}')"`, { stdio: 'inherit' });

console.log('=== Install Complete ===');
console.log('Run "Start" to launch the app.');
