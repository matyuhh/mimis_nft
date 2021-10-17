from brownie import Collectible, network, config, accounts
from scripts.helper_fund_collectible import get_breed

mimis_metadata_dic = {
    "ZIRA": "https://ipfs.io/ipfs/QmcDGoWqhS627xhSKq81fb21pTwGRd896HbtKAjnqEGzGU?filename=1-ZIRA.json",
    "SARITA": "https://ipfs.io/ipfs/QmSj1uzaBrb8anBgDS9xi6rEcFmCmesW6JgEWs392xToLb?filename=0-SARITA.json"
}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
    print("Working on " + network.show_active())
    collectible = Collectible[len(Collectible) - 1]
    number_of_collectibles = collectible.tokenCounter()
    print(number_of_collectibles)
    for token_id in range(number_of_collectibles):
        breed = get_breed(collectible.tokenIdToBreed(token_id))
        if not collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, collectible, mimis_metadata_dic[breed])
        else:
            print("Already set that tokenURI: {}".format(token_id))

def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id))
    )
    print("Please wait to 20 minutes, and hit the 'refresh metadata' button.")