const { API_KEY, PRIVATE_KEY, CONTRACT_ADDRESS, FLAG } = process.env;
const {
  ethers
} = require("hardhat");

const contract = require("../artifacts/contracts/aBakery.sol/ABakery.json");
const provider = new ethers.providers.AlchemyProvider(network = "goerli", API_KEY);
const signer = new ethers.Wallet(PRIVATE_KEY, provider);
const aBakery = new ethers.Contract(CONTRACT_ADDRESS, contract.abi, signer);


async function main() {
  await aBakery.setPastry(FLAG);
  await aBakery.addFlavor(0, 'drottningsylt');
  await aBakery.addFlavor(1, 'hallon');
  await aBakery.addFlavor(2, 'blåbär');
}


main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });