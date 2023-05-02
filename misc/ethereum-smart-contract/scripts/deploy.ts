async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  console.log("Account balance:", (await deployer.getBalance()).toString());

  const ABakery = await ethers.getContractFactory("ABakery");
  const aBakery = await ABakery.deploy();

  console.log("Contract (ABakery) address:", aBakery.address);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => { 
  process.exitCode = 1;
});