#!/bin/bash

cd ctf-flag

# Copy live config to deploy
cp hardhat.config.ts.live hardhat.config.ts
cp .env.owner .env

# Deploy contract
npx hardhat --network goerli run scripts/deploy.ts

# Make sure to update the .env files with the new contract adress