from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_VALUE = 200000000000

# this helpful_scripts.py script is where we store useful functions that we will want to deploy across scripts
def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    # when deployment is in development, will need to spin up a mock aggregator and use the appropriate arguments as well.  price feed will now be based on mock aggregator address not the test network address
    print(f"the active network is {network.show_active()}")
    print("depploying mock aggregatorV3interface")
    # AggregatorV3Interface requires arguments so will need to provide apart from accounts address for deployment

    # only deploy mock if there is none deployed yet in the network
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS,
            STARTING_VALUE,
            {"from": get_account()},
        )
    print("MockAggregator is deployed!!")
