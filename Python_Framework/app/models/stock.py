from db import db

class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    number = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, name, number, price):
        self.name = name
        self.number = number
        self.price = price

    def json(self):
        return {'name': self.name, 'number': self.number, 'price':self.price}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()
