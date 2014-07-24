from app import db

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(120), index = True)
    twitter = db.Column(db.String(120))
    phone = db.Column(db.String(15))
    carrier = db.Column(db.String(120))

    def __repr__(self):
        return '<Communication %r>' % (self.name)
