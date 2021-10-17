from brownie import Collectible, network
from metadata import sample_metadata
from scripts.helper_fund_collectible import get_breed
from pathlib import Path
import os
import requests
import json

def main():
    print("Working on " + network.show_active())
    collectible = Collectible[len(Collectible) - 1]
    number_of_tokens = collectible.tokenCounter()
    print("The number of tokens you've deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, collectible)

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        breed = get_breed(nft_contract.tokenIdToBreed(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) + str(token_id) + "-" + breed + ".json"
        )
        if Path(metadata_file_name).exists():
            print("{} already found!".format(metadata_file_name))
        else:
            print("Creating Metadata File {}".format(metadata_file_name))
            collectible_metadata["name"] = get_breed(nft_contract.tokenIdToBreed(token_id))

            if collectible_metadata["name"] == "ZIRA":
                collectible_metadata["description"] = "The best mimi!"
            else:
                collectible_metadata["description"] = "A badass mini..."

            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.jpg".format(breed.lower())
                image_to_upload = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(uri)
        return uri
    return None
        