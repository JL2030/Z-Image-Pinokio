// Z-Image-Turbo Link Script for Pinokio
// Creates symlinks for the app

const path = require('path');
const fs = require('fs');

const APP_PATH = __dirname;

console.log('=== Z-Image-Turbo Link ===');

// Create necessary directories
const dirs = ['model', 'output', 'temp'];
dirs.forEach(dir => {
  const dirPath = path.join(APP_PATH, dir);
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`Created: ${dir}`);
  }
});

console.log('=== Link Complete ===');
