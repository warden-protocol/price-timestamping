//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract PriceHashStorage {

    // state variables
    address private owner;
    uint public totalPriceHashes = 0;
    uint public fee;
    
    struct PriceHash {
        address sender;
        string hash;
        uint timestamptz;
    }

    PriceHash[] public PriceHashes; //declaring it public will default in a GET function when deploying, so no need to write it

    modifier onlyOwner {
        require(msg.sender == owner);
        _; //run the function
    }

    constructor() {
        owner = msg.sender;
        fee = 0; //we could include a fee later, but doesn't make sense if we are the only ones storing
    }

    function storePriceHash(string memory _hash, uint _timestamptz) public payable {
        require(msg.value >= fee, "Insufficient Balance"); //always true since 0 fee for now
        PriceHash memory newPriceHash = PriceHash(msg.sender,_hash,_timestamptz);
        PriceHashes.push(newPriceHash);
        totalPriceHashes ++;
    }

    function getContractBalance() public view returns(uint){
        return address(this).balance;
    }

    function setFee(uint _fee) public onlyOwner(){
        fee = _fee; //to change view after contract deployment
    }
   
    function withdraw(uint _amount) public payable onlyOwner {
        payable(owner).transfer(_amount);
    }

}