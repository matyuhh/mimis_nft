from brownie import Collectible, accounts, config
from scripts.helper_fund_collectible import get_breed
import time

STATIC_SEED = 123

def main():
    dev = accounts.add(config['wallets']['from_key'])
    collectible = Collectible[len(Collectible) - 1]
    transaction = collectible.createCollectible(STATIC_SEED, "None", {"from": dev})
    transaction.wait(1)
    requestId = transaction.events['requestedCollectible']['requestId']
    token_id = collectible.requestIdToTokenId(requestId)
    time.sleep(35)
    breed = get_breed(collectible.tokenIdToBreed(token_id))
    print('Mimi breed of tokenId {} is {}'.format(token_id, breed))
