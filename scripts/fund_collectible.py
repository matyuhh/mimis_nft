from brownie import Collectible
from scripts.helper_fund_collectible import fund_collectible

def main():
    collectible = Collectible[len(Collectible) - 1]
    fund_collectible(collectible)