from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
from flask_marshmallow import Marshmallow
from datetime import datetime
from credentials import URI

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    countries = db.Column(db.String(100))
    hashrate = db.Column(db.String(100))
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'),
                        nullable=False)
    coin = db.relationship('Coin',
                           backref=db.backref('pools', lazy=True))

    def __repr__(self):
        return '<Pool %r>' % self.url


# DATABASE MODELS
class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)
    price = db.Column(db.String(100), nullable=False)
    network_hashrate = db.Column(db.String(100), nullable=False)
    algo = db.Column(db.String(100))
    reward = db.Column(db.String(100))
    time = db.Column(db.String(100))

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithm.id'),
                             nullable=False)
    algorithm = db.relationship('Algorithm',
                                backref=db.backref('coins', lazy=True))

    def __repr__(self):
        return '<Coin %r>' % self.name


class Miner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    coin = db.Column(db.String(100))
    hashrate = db.Column(db.String(100))
    power = db.Column(db.String(100))
    algo = db.Column(db.String(100))

    algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithm.id'),
                             nullable=False)
    algorithm = db.relationship('Algorithm',
                                backref=db.backref('miners', lazy=True))

    def __repr__(self):
        return '<Miner %r>' % self.name


class Algorithm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return '<Coin %r>' % self.coins


##############

# SCHEMAS #

class PoolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pool
        include_fk = True


class CoinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Coin
        include_fk = True


class MinerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Miner
        include_fk = True


class AlgorithmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Algorithm
        include_fk = True


pool_schema = PoolSchema()
pools_schema = PoolSchema(many=True)

coin_schema = CoinSchema()
coins_schema = PoolSchema(many=True)

miner_schema = MinerSchema()
miners_schema = MinerSchema(many=True)

algorithm_schema = AlgorithmSchema()
algorithms_schema = AlgorithmSchema(many=True)

###########

# API


def abort_if_coin_doesnt_exist(code):
    if Coin.query.filter_by(code=code).first() is None:
        abort(404, message="Coin {} doesn't exist".format(code))


def abort_if_algo_doesnt_exist(name):
    if Algorithm.query.filter_by(name=name).first() is None:
        abort(404, message="Coin {} doesn't exist".format(name))


class AlgoInfo(Resource):
    def get(self, name):
        abort_if_algo_doesnt_exist(name)
        algo = Algorithm.query.filter_by(name=name).first()
        minerArr = []
        for miner in algo.miners:
            minerArr.append(miner_schema.dump(miner))
        coinArr = []
        for coin in algo.coins:
            coinArr.append(coin_schema.dump(coin))
        return {'info': algorithm_schema.dump(algo), 'coins': coinArr, 'miners': minerArr}


class AlgoInfoList(Resource):
    def get(self):
        algos = Algorithm.query.all()
        algoArr = []
        for algo in algos:
            algoArr.append(algorithm_schema.dump(algo))
        return algoArr


class CoinInfo(Resource):
    def get(self, code):
        abort_if_coin_doesnt_exist(code)
        coin = Coin.query.filter_by(code=code).first()
        poolArr = []
        for pool in coin.pools:
            poolArr.append(pool_schema.dump(pool))

        minerArr = []
        for miner in coin.algorithm.miners:
            minerArr.append(miner_schema.dump(miner))

        return {'info': coin_schema.dump(coin), 'pools': poolArr, 'miners': minerArr}


class CoinInfoList(Resource):
    def get(self):
        coins = Coin.query.all()
        coinArr = []
        for coin in coins:
            coinArr.append(coin_schema.dump(coin))
        return coinArr


# Basic HTML for home page
@app.route("/")
def home():
    return "<h1>You've Reached the Cryptocurrency Energy Consumption Index Data API</h1>"


api.add_resource(AlgoInfo, '/algorithms/<name>')
api.add_resource(AlgoInfoList, '/algorithms')

api.add_resource(CoinInfo, '/coins/<code>')
api.add_resource(CoinInfoList, '/coins')

if __name__ == '__main__':
    app.run()
