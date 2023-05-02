const { API_KEY, PRIVATE_KEY, CONTRACT_ADDRESS } = process.env;
const {
  ethers
} = require("hardhat");

const contract = require("../artifacts/contracts/aBakery.sol/ABakery.json");
const provider = new ethers.providers.AlchemyProvider(network = "goerli", API_KEY);
const signer = new ethers.Wallet(PRIVATE_KEY, provider);
const aBakery = new ethers.Contract(CONTRACT_ADDRESS, contract.abi, signer);

async function main() {

  const pastry = await aBakery.pickupOrderedPastry();
  console.log("The flag is: ", pastry);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });