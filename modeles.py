from app import db



association_table = db.Table('association',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                             db.Column('products_id', db.Integer, db.ForeignKey('product.id'))
                             )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    roles = db.relationship('Role', backref='user', lazy=True)
    products = db.relationship('Product', secondary=association_table, backref='users', lazy='dynamic')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False)
    prix = db.Column(db.Float, nullable=False)

db.create_all()
