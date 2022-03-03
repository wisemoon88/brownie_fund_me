from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()

    # deploy function will need to check what network the contract is being deployed to, if on development, deploy mock
    # since contract is now not using hardcoded address, will need to send the address as an argument during deployment so argumennt can be retrieved by constructor
    # check for active network which now also includes a local ganache blockchain which needs to be considered as local not testnet
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # importingn deploy mocks from helpful scripts instead of hardcodnig here
        deploy_mocks()
        # pricefeed is now based on mock deployed address not test network address
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"contract deployed to {fund_me.address} ")
    return fund_me


# NOTE:  verified contract was deployed at 0x989a0D7Bf3CA876F73F3892Ca648C2aC7BCC4B3A
def main():
    deploy_fund_me()
