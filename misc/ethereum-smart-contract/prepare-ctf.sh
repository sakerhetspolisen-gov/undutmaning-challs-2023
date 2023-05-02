#!/bin/bash

cd ctf-flag

# Copy live config to deploy
cp hardhat.config.ts.live hardhat.config.ts
cp .env.owner .env

# Set pastry (of the daY) and add the (stolen) flavor to the contract
npx hardhat --network goerli run scripts/set-pasty-of-the-day-and-flavor.js