// Z-Image-Turbo Torch Installation for Pinokio
// Handles PyTorch installation with CUDA support

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const ENV_PATH = path.join(__dirname, 'env');
const pipPath = path.join(ENV_PATH, 'Scripts', 'pip.exe');

console.log('=== Installing PyTorch ===');

// Detect CUDA version
let cudaVersion = 'cu121';
try {
  const nvidiaSmi = execSync('nvidia-smi', { encoding: 'utf-8' });
  const match = nvidiaSmi.match(/CUDA Version: (\d+\.\d+)/);
  if (match) {
    const version = match[1];
    console.log(`Detected CUDA ${version}`);
    if (version.startsWith('12.')) {
      cudaVersion = 'cu121';
    } else if (version.startsWith('11.')) {
      cudaVersion = 'cu118';
    }
  }
} catch (e) {
  console.log('nvidia-smi not found, using default CUDA version');
}

// Install PyTorch
console.log(`Installing PyTorch with ${cudaVersion}...`);
execSync(`"${pipPath}" install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/${cudaVersion}`, { stdio: 'inherit' });

console.log('=== PyTorch Installed ===');
