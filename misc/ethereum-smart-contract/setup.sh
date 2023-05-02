#!/bin/bash

# Uncomment if to install node.js
# sudo apt update
# sudo apt install curl git
# curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
# sudo apt-get install -y nodejs

# Create a directory to compile to source code
mkdir ctf-flag
cd ctf-flag

# Setup node.js and hardhat (select defaults)
npm init
npm install --save-dev hardhat
npm install dotenv --save
# Select typescript projects
npx hardhat

# Copy source code
cp ../contracts/* contracts/
cp ../scripts/* scripts/
cp ../test/* test/
cp ../.env.* ../hardhat.config.ts.* .

# Compile the contract
npx hardhat compile

# Copy test config to run tests
cp hardhat.config.ts.test hardhat.config.ts

# Run tests
npx hardhat test