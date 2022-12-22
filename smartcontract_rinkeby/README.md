Great tutorial for eth smart contract deployment with react js frontend: https://www.youtube.com/watch?v=Qu6GloG0dQk&t=1541s
Smart contract deployment starts here: https://www.youtube.com/watch?v=Qu6GloG0dQk&t=1650s

install Node.js/npm, truffle and other dependencies:
```console
brew install node
npm i -g truffle
npm i dotenv 
npm i @truffle/hdwallet-provider
```
initialize project (for this repo already done)
```console
#npm init
#truffle init
```
add .env file
```console
echo  PRIVATE_KEY=key_wallet_with_goerli_funds > .env
echo  INFURA_API_URL=infura_io_url_needed_only_for_deployment >> myfile.txt
```

deploy smart contract to goerli test network
```console
truffle migrate --network goerli   
```