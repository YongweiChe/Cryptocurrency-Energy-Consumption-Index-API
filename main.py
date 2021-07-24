from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    countries = db.Column(db.String())
    hashrate = db.Column(db.String())
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'),
                        nullable=False)
    coin = db.relationship('Coin',
                           backref=db.backref('pools', lazy=True))

    def __repr__(self):
        return '<Pool %r>' % self.url


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    code = db.Column(db.String(), unique=True)
    price = db.Column(db.String(), nullable=False)
    network_hashrate = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithm.id'),
                             nullable=False)
    algorithm = db.relationship('Algorithm',
                                backref=db.backref('coins', lazy=True))

    def __repr__(self):
        return '<Coin %r>' % self.name


class Miner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    coin = db.Column(db.String())
    hashrate = db.Column(db.String())
    power = db.Column(db.String())
    algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithm.id'),
                             nullable=False)
    algorithm = db.relationship('Algorithm',
                                backref=db.backref('miners', lazy=True))

    def __repr__(self):
        return '<Miner %r>' % self.name


class Algorithm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __repr__(self):
        return '<Coin %r>' % self.coins


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

if __name__ == '__main__':
    app.run(debug=False)
