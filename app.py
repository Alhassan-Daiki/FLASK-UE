from curses import flash
from urllib import request
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
bootstrap = Bootstrap(app)


db = SQLAlchemy(app)
from modeles import User, Product, Role

migrate = Migrate(app, db)

def create_app():
    db.init_app(app)


@app.route('/')
def index():
    return render_template('base.html')

#Afficher la liste des utilisateurs

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users/index.html', users=users)

#Afficher le détail d'un utilisateur
@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)




# Ajouter un utilisateur
@app.route('/users/create', methods=['GET', 'POST'])
def user_create():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        user = User(nom=nom, prenom=prenom, email=email)
        user.set_password(password)  # hashage du mot de passe
        db.session.add(user)
        db.session.commit()
        flash('L\'utilisateur a été créé avec succès', 'success')
        return redirect(url_for('users'))
    return render_template('users/create.html')


#Modifier un utilisateur
@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.nom = request.form['nom']
        user.prenom = request.form['prenom']
        user.email = request.form['email']
        db.session.commit()
        flash('L\'utilisateur a été modifié avec succès', 'success')
        return redirect(url_for('user_detail', user_id=user.id))
    return render_template('users/edit.html', user=user)

#Supprimer un utilisateur
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('L\'utilisateur a été supprimé avec succès', 'success')
    return redirect(url_for('users'))


@app.route('/roles')
def roles():
    roles = Role.query.all()
    return render_template('roles/index.html', roles=roles)

#Afficher le détail d'un role
@app.route('/roles/<int:role_id>')
def role_detail(role_id):
    role = Role.query.get_or_404(role_id)
    return render_template('roles/detail.html', role=role)

#Ajouter un role
@app.route('/roles/create', methods=['GET', 'POST'])
def role_create():
    if request.method == 'POST':
        nom = request.form['nom']
        role = Role(nom=nom)
        db.session.add(role)
        db.session.commit()
        flash('Le rôle a été créé avec succès', 'success')
        return redirect(url_for('roles'))
    return render_template('roles/create.html')


#Modifier un role
@app.route('/roles/<int:role_id>/edit', methods=['GET', 'POST'])
def role_edit(role_id):
    role = Role.query.get_or_404(role_id)
    if request.method == 'POST':
        role.nom = request.form['nom']
        role.user_id = request.form['user_id']
        db.session.commit()
        flash('Le role a été modifié avec succès', 'success')
        return redirect(url_for('role_detail', role_id=role.id))
    users = User.query.all()
    return render_template('roles/edit.html', role=role, users=users)

#Supprimer un role
@app.route('/roles/<int:role_id>/delete', methods=['POST'])
def role_delete(role_id):
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    flash('Le role a été supprimé avec succès', 'success')
    return redirect(url_for('roles'))


# Read all products
@app.route('/show_products')
def show_products():
    products = Product.query.all()
    return render_template('products/show_products.html', products=products)



# Read a product
@app.route('/product/<int:id>')
def show_product(id):
    product = Product.query.get(id)
    seller = product.seller
    return render_template('products/show_product.html', product=product, seller=seller)

# Create a product
@app.route('/product/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        seller_id = request.form['seller_id']
        product = Product(name=name, price=price, seller_id=seller_id)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('show_products'))
    else:
        users = User.query.all()
        return render_template('products/create_product.html', users=users)


# Update a product
@app.route('/product/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get(id)
    users = User.query.all()
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.seller_id = request.form['seller_id']
        db.session.commit()
        return redirect(url_for('show_product', id=id))
    return render_template('products/update_product.html', product=product, users=users)


# Delete a product
@app.route('/product/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('show_products'))


if __name__ == '__main__':
    create_app()
    app.run(debug=True)



