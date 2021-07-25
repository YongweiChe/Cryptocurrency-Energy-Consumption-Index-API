from bs4 import BeautifulSoup
from main import db
from main import Pool, Coin, Miner, Algorithm
import os


def getCoinInfo():
    file = open("CoinStats/home.txt", "r")

    soup = BeautifulSoup(file.read(), 'html.parser')
    coins = soup.find(id="coins").find_all("tr", class_=["odd", "even"])
    for coin in coins:
        code = coin.find(class_='homeurl').find('small').get_text()
        algorithm = coin.find(class_='sorting_1').previous_sibling.find('div').get_text()
        name = coin.find(class_='homeurl').find('b').get_text()
        price = coin.find(class_='show1050').find('span').get_text()
        network_hashrate = coin.find(class_='show1350').find('span').get_text()

        algoDB = Algorithm.query.filter_by(name=algorithm).first()
        if algoDB is None:
            algoDB = Algorithm(name=algorithm)

        coinDB = Coin.query.filter_by(code=code).first()
        if coinDB is None:
            coinDB = Coin(name=name, code=code, price=price, network_hashrate=network_hashrate, algorithm=algoDB)
            db.session.add(coinDB)
        else:
            coinDB.name = name
            coinDB.price = price
            coinDB.network_hashrate = network_hashrate
            coinDB.algorithm = algoDB
    db.session.commit()


def getPoolInfo(path):
    file = open(path, "r")

    # getting associated coin
    start = path.find('/')
    end = path.find('.')
    coin = path[start + 1:end]
    coinDB = Coin.query.filter_by(name=coin).first()
    soup = BeautifulSoup(file.read(), 'html.parser')

    try:
        pools = soup.find(id="pools").find_all("tr", class_=["odd", "even"])
        for pool in pools:
            name = pool.find("b").find("a").get_text()
            countries = pool.find(class_="tooltiptext1").get_text()
            hashrate = pool.find(class_="sorting_1").get_text()

            Pool(url=name, countries=countries, hashrate=hashrate)
            poolDB = Pool.query.filter_by(coin=coinDB, url=name).first()
            if poolDB is None:
                poolDB = Pool(url=name, countries=countries, hashrate=hashrate, coin=coinDB)
                db.session.add(poolDB)
            else:
                poolDB.countries = countries
                poolDB.hashrate = hashrate
    finally:
        print(coin + 'pools updated')

    db.session.commit()


def getMinerInfo(path):
    file = open(path, "r")

    # getting coin code
    start = path.find('/')
    end = path.find('.')
    coin = path[start + 1:end]

    soup = BeautifulSoup(file.read(), 'html.parser')

    miners = soup.find(id="listContainer").find(class_="list-body").find_all("div", class_="list-row")

    for miner in miners:
        name = miner.attrs['data-name']
        hashrate = miner.find("div", {"data-key": "hashrate"}).find(class_="d-none").get_text()
        power = miner.find("div", {"data-key": "power"}).get_text()

        Miner(name=name, coin=coin, hashrate=hashrate, power=power)

        coinDB = Coin.query.filter_by(code=coin).first()
        if coinDB is not None:
            algoDB = coinDB.algorithm
            minerDB = Miner.query.filter_by(name=name, algorithm=algoDB).first()
            if minerDB is None:
                minerDB = Miner(name=name, hashrate=hashrate, power=power, coin=coinDB.code, algorithm=algoDB)
                db.session.add(minerDB)
            else:
                minerDB.hashrate = hashrate
                minerDB.power = power
    print(coin + " Hardware Updated")
    db.session.commit()


def InsertPoolsIntoDB():
    for filename in os.listdir('PoolStats'):
        if filename.endswith(".txt"):
            path = os.path.join('PoolStats', filename)
            getPoolInfo(path)
            continue
        else:
            continue


def InsertMinersIntoDB():
    for filename in os.listdir('MinerStats'):
        if filename.endswith(".txt"):
            path = os.path.join('MinerStats', filename)
            getMinerInfo(path)
            continue
        else:
            continue


# UPDATES DATABASES FULLY
def main():
    getCoinInfo()
    InsertPoolsIntoDB()
    InsertMinersIntoDB()


if __name__ == "__main__":
    main()