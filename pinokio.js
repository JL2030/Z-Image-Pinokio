// Z-Image-Turbo Pinokio Integration
// Main entry point for Pinokio

const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const APP_PATH = __dirname;

// Pinokio API
const pinokio = {
  local: {
    set: (key, value) => {
      console.log(`[pinokio] local.set: ${key} = ${value}`);
    },
    get: (key) => {
      console.log(`[pinokio] local.get: ${key}`);
      return null;
    },
  },
};

console.log('=== Z-Image-Turbo for Pinokio ===');

// Check if installed
const envPath = path.join(APP_PATH, 'env');
if (!fs.existsSync(envPath)) {
  console.log('Not installed. Running install...');
  require('./install.js');
} else {
  console.log('Already installed. Starting...');
  require('./start.js');
}
