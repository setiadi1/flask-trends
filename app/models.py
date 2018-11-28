from datetime import datetime, date
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Text, nullable=False)
    order_date = db.Column(db.Date, nullable=False, index=True)
    ship_date = db.Column(db.Date, nullable=False, index=True)
    ship_mode = db.Column(db.Text, nullable=False)
    customer_id = db.Column(db.Text, nullable=False)
    customer_name = db.Column(db.Text, nullable=True)
    segment = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=True)
    state = db.Column(db.Text, nullable=True)
    country = db.Column(db.Text, nullable=True)
    postal_code = db.Column(db.Integer, nullable=True)
    market = db.Column(db.Text, nullable=True)
    region = db.Column(db.Text, nullable=True)
    product_id = db.Column(db.Text, nullable=True)
    category = db.Column(db.Text, nullable=True)
    sub_category = db.Column(db.Text, nullable=True)
    product_name = db.Column(db.Text, nullable=True)
    sales = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Text, nullable=True)
    discount = db.Column(db.Text, nullable=True)
    profit = db.Column(db.Text, nullable=True)
    shipping_cost = db.Column(db.Text, nullable=True)
    order_priority = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Orders('{self.order_id}', '{self.order_date}', '{self.ship_date}', '{self.ship_mode}', '{self.customer_id}', '{self.customer_name}', '{self.segment}', '{self.city}', '{self.state}', '{self.country}', '{self.postal_code}', '{self.market}', '{self.region}', '{self.product_id}', '{self.category}', '{self.sub_category}', '{self.product_name}', '{self.sales}', '{self.quantity}', '{self.discount}', '{self.profit}', '{self.shipping_cost}', '{self.order_priority}')"

