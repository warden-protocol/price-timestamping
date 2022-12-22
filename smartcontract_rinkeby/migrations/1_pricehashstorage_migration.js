const PriceHashStorage = artifacts.require("PriceHashStorage");

module.exports = function (deployer) {
  deployer.deploy(PriceHashStorage);
};
