// Z-Image-Turbo Start Script for Pinokio
// Launches the Gradio app

const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const APP_PATH = __dirname;
const ENV_PATH = path.join(APP_PATH, 'env');
const pythonPath = path.join(ENV_PATH, 'Scripts', 'python.exe');

console.log('=== Z-Image-Turbo Start ===');

// Check if env exists
if (!fs.existsSync(ENV_PATH)) {
  console.error('Virtual environment not found. Please run Install first.');
  process.exit(1);
}

// Set environment variables
process.env.Z_IMAGE_MODEL_PATH = path.join(APP_PATH, 'model');

// Launch the app
const app = spawn(pythonPath, [path.join(APP_PATH, 'app', 'app.py')], {
  stdio: 'inherit',
  env: process.env,
});

app.on('close', (code) => {
  console.log(`App exited with code ${code}`);
  process.exit(code);
});

// Handle Ctrl+C
process.on('SIGINT', () => {
  app.kill('SIGINT');
});
