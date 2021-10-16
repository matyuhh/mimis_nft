from brownie import Collectible, accounts, network, config, interface

def fund_collectible(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])
    link_token = interface.LinkTokenInterface(config['networks'][network.show_active()]['link_token'])
    link_token.transfer(nft_contract, 1000000000000000000, {"from": dev})

def get_breed(breed_number):
    switch = {0: 'ZIRA', 1:'SARITA'}
    return switch[breed_number]

    