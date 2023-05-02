# Smart Contract on the Ethereum blockchain

## 1.1 Description

A follow-up on the social media CTF with a deployed smart contract on the Ethereum (testnet) blockchain. The smart 
contract is a piece of code that when executed correctly (in a transaction with some test Ethereum money) returns the flag.

The history of the vicious `ensockerbagare` that is about to open a new bakery `aBakery` in the form of a smart contract 
on the Ethereum blockchain where customer can buy the daily pastry in different flavors. As this is a CTF the contract is 
deployed on the Goerli testnet (https://goerli.net/) so anyone can create a wallet and can freely faucet 0.2 ETH per day 
in order to buy a pastry from the bakery.

## 1.2 Public description

Ett bageri

## 1.3 How to 'build'

The CTF user should find alot of examples on how to interact with a smart contract on the Ethereum blockchain on the web.

**OBS THE CONTRACT HAS ALREADY BEEN DEPLOYED AND IS PREPARED**

1. Update the `.env.owner` with the correct data

2. Set up the development environment (install node.js, hardhat, copy source and run tests). Select "TypeScript project"
```commandline
./setup.sh
```

3. Deploy the smart contract on the Ethereum blockchain (update the .env files with the new contract adress)
```commandline
./deploy.sh
```

4. Prepare the smart contract with the pasty of the day `the flag` and the hint `drottningsylt` and add two flavor `hallon` and `blåbär`
```commandline
./prepare-ctf.sh
```

5. Make an order (with a test user). The transaction take a few minutes to complete before the order can be "picked up"
```commandline
./test-ctf-order.sh
```

6. Pick up the order (with a test user). If the user get the error `You haven't ordered any pastry (yet).`, the transaction
is not processed yet
```commandline
./test-ctf-pickup.sh
```

## 1.4 Storyline

`Mycket tyder på att den ondsinte sockerbagaren lyckades få ut en av Haralds topphemliga smaktillsatser. Vår underrättelse  pekar på att sockerbagaren är på väg att etablera ett bageri vid stationen på Görlitzer Park i Berlin. Signalspaningen har även fångat denna misstänkta adress 0x038996c8864EF0378A261D8E990abAA92881B671`

## 1.5 Steps

Using tools like `https://goerli.etherscan.io/` and searching for the address `0x038996c8864EF0378A261D8E990abAA92881B671` 
the CTF user will see that the `ensockerbagares` wallet has some transaction and that one is for a `smart contract`.

By opening the transaction for the `smart contract` the CTF user can start investigating the contract source code
(deployed together with the contract). The CTF user must write a small script to extract the flag (can partly execute 
some functions directly on `Etherscan`, but is not able to read the result (the flag)).

Use the (online) tool `Remix`, copy the contract source code, connect a `MetaMask` wallet (loaded with some Goerli ETH
from `Goerli Faucet`) and connect `Remix` to the contract public address. Use `Remix` to call the function 
`getFlavors` to get the hint `drottningsylt` (with the ingredients `blåbär` and `hallon`), the place an order and pick
it up.

## 1.6 How to solve

Görlitzer Park (nicknamed "Görli"), and without `ö` is Goerli. Ethereum testnets are often namen after train stations
(as the closed testnets Rinkeby and Ropsten). Goerli (named after the train station in Görlitzer Park) is one of the 
largest and most active Ethereum testnets, and the last to transition to proof-of-stake (PoS).

The numbers `0x038996c8864EF0378A261D8E990abAA92881B671` is an Ethereum wallet address (have a length of 40 hexadecimal 
characters and begin with “0x”).

## 1.7 Easy/Medium

## 1.8 Hint

* Remix, MetaMask, Goerli Faucet (tools that may help to solve the challenge)
* `Ingredienser i drottningsylt` (`blåbär` and `hallon` is two accepted flavors when ordering a pastry)

## Accounts

* The email account (in order to create wallets etc.):

  * url: XXXXXXXXXXXXXXXXXXXXXXX
  * user: XXXXXXXXXXXXXXXXXXXXXXX
  * pass: XXXXXXXXXXXXXXXXXXXXXXX

* Alchemy account in order to make requests to the Ethereum blockchain. Alchemy is a blockchain dev platform whose API 
lets you connect to the Ethereum blockchain without needing to run your own nodes.

* url: alchemy.com
  * user: XXXXXXXXXXXXXXXXXXXXXXX
  * pass: XXXXXXXXXXXXXXXXXXXXXXX
  * app: CTF app (Goerli testnet)
  * api: XXXXXXXXXXXXXXXXXXXXXXX

* To carry out transactions we must have an Ethereum wallet. In this case we use MetaMask for Ethereum (chrome plugin)

  * user: XXXXXXXXXXXXXXXXXXXXXXXXX
  * pass: XXXXXXXXXXXXXXXX
  * phrase: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  * account: XXXXXXXXXXXXXXXXXXXXXXX
  * network: goerli
  * wallet address: XXXXXXXXXXXXXXXXXXXX
  * wallet private key: XXXXXXXXXXXXXXXXXX

* Add (fake) ETH from a faucet. To acquire some fake ETH we use GOERLI FAUCET. Copy your wallet address and past it to 
get 0.2 GoerliETH

  * url: goerlifaucet.com
  * user: XXXXXXXXXXXXXXXXXXXXXXX
  * pass: XXXXXXXXXXXXXXXXXXXXXXX

* GitHub account to store the contract source (not in use)  

  * https://github.com/XXXXXXXXXXXX
  * user: XXXXXXXXXXXXXXXXXXXX
  * pass: XXXXXXXXXXXXXXXXXXXX
