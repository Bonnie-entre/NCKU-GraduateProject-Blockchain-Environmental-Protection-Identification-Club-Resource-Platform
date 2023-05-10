const { ethers } = require("ethers");
const fs = require("fs");
require("dotenv").config({ path: "../.env" });

const ethersPath = require.resolve('ethers')
console.log(`the path:${ethersPath}`)

async function UploadPicture(){
    //Connect to chain and wallet
    const provider = new ethers.providers.JsonRpcProvider(process.env.SEPOLIA_RPC_URL);
    let walletInstance = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
    const signer = walletInstance.connect(provider);

    //Connect to contract
    const abi = fs.readFileSync(
    "../contracts/contracts_EFToken_sol_EFToken.abi",
    "utf8"
    );
    const contractAddress = process.env.EFToken_ContractAddress;
    const contract = new ethers.Contract(contractAddress, abi, signer);

    //call contract function - UploadPicture
    let uploadPic_Response = await contract.UploadPicture(
      _clubID,
      _activityID,
      _activityName,
      _date,
      _picID,
      _picNum,
      _base64
    )
    let uploadPic_Receipt = await uploadPic_Response.wait(1)
    console.log(`Check uploadPicture on blockchain: ${uploadPic_Receipt}`);
    console.log(`Get hash: ${uploadPic_Receipt.transactionHash}`);

    return uploadPic_Receipt.transactionHash
}


async function Owner(){
  const ethersPath = require.resolve('ethers')
console.log(`the path:${ethersPath}`)
    //Connect to chain and wallet
    const provider = new ethers.providers.JsonRpcProvider(process.env.SEPOLIA_RPC_URL);
    let walletInstance = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
    const signer = walletInstance.connect(provider);

    //Connect to contract
    const abi = fs.readFileSync(
    "./contracts/contracts_EFToken_sol_EFToken.abi",
    "utf8"
    );
    const contractAddress = process.env.EFToken_ContractAddress;
    const contract = new ethers.Contract(contractAddress, abi, signer);

    // call contract - owner()
      const owner = await contract.owner()
      console.log(`Owner is ${owner}`)
}

// Owner()

module.exports = { Owner }