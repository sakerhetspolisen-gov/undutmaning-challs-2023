#!/bin/bash

cd ctf-flag

# Copy live config to deploy
cp hardhat.config.ts.live hardhat.config.ts
cp .env.testuser .env

# Pick up the orders pastry
npx hardhat --network goerli run scripts/pickup-pastry.js