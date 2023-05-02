const { API_KEY, PRIVATE_KEY, CONTRACT_ADDRESS } = process.env;
const {
  ethers
} = require("hardhat");

const contract = require("../artifacts/contracts/aBakery.sol/ABakery.json");
const provider = new ethers.providers.AlchemyProvider(network = "goerli", API_KEY);
const signer = new ethers.Wallet(PRIVATE_KEY, provider);
const aBakery = new ethers.Contract(CONTRACT_ADDRESS, contract.abi, signer);

async function main() {

  // A pastry costs 10000 gwei GoerliETH
  const fee = ethers.utils.parseEther("0.00001");
  await aBakery.connect(signer).orderPastry('blåbär', {value: fee});
  console.log("You have to wait a while until the transaction is complete before you can pickup you order.");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });