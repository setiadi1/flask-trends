import os
import io
import base64
import secrets
import warnings
import itertools
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import date, datetime
from sqlalchemy import desc, asc, func
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, TestFrom
from app.models import User, Post, Orders
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/trends", methods=['GET', 'POST'])
def trends():
    if current_user.is_authenticated:
        # start = date(year=2013,month=11,day=1)
        # end = date(year=2013,month=11,day=3)
        # dated = Orders.query.filter(Orders.order_date >= start).filter(Orders.order_date <= end).filter_by(category='Furniture').order_by(asc(Orders.order_date))
        # date = Orders.query.filter(order_date.between('2013-01-01', '2013-02-01'))
        # form = RegistrationForm()
        # datax = form.category.data

        cat = Orders.query.with_entities(Orders.category).group_by(Orders.category).all()
        states = Orders.query.with_entities(Orders.state).filter_by(country="United States").group_by(Orders.state).all()
        return render_template('tr.html', cat=cat, states=states)
    if current_user.is_anonymous:
        return render_template('unauthenticated.html')

@app.route("/_trends", methods=['GET', 'POST'])
def _trends():

    category = request.form['category']
    state = request.form['state']
    od_start = request.form['start']
    od_end = request.form['end']
    if od_start and od_end:
        start = datetime.strptime(od_start, '%d-%m-%Y').strftime('%Y-%m-%d')
        end = datetime.strptime(od_end, '%d-%m-%Y').strftime('%Y-%m-%d')
    granularity = request.form['granularity']

    text1 = "Category, Office Supplies"
    text2 = 'Whenever you need to, be sure to use margin utilities to keep things nice and tidy. This example text is going to run a bit longer so that you can see how spacing within an alert works with this kind of content. Be sure you’ve loaded the alert plugin, or the compiled Bootstrap JavaScript'
    text3 = 'Trends'
    text4 = 'Prediction'

    orders = Orders.query.filter(Orders.order_date >= start).filter(Orders.order_date <= end).filter_by(category='Furniture').order_by(asc(Orders.order_date))

    data_list = []
    for v in orders:
        odx = datetime.strptime(str(v.order_date), '%Y-%m-%d').strftime('%Y-%m-%d')
        sdx = datetime.strptime(str(v.ship_date), '%Y-%m-%d').strftime('%Y-%m-%d')
        id = v.id
        order_id = str(v.order_id)
        order_date = odx
        ship_date = sdx
        ship_mode = str(v.ship_mode)
        customer_id = str(v.customer_id)
        customer_name = str(v.customer_name)
        segment = str(v.segment)
        city = str(v.city)
        state = str(v.state)
        country = str(v.country)
        postal_code = str(v.postal_code)
        market = str(v.market)
        region = str(v.region)
        product_id = str(v.product_id)
        category = str(v.category)
        sub_category = str(v.sub_category)
        product_name = str(v.product_name)
        sales = v.sales
        quantity = v.quantity
        discount = v.discount
        profit = v.profit
        shipping_cost = v.shipping_cost
        order_priority = str(v.order_priority)

        op = (id, order_id, order_date, ship_date, ship_mode, customer_id, customer_name, segment, city, state, country, postal_code, market, region, product_id, category, sub_category, product_name, sales, quantity, discount, profit, shipping_cost, order_priority)

        data_list.append(op)

    df = pd.DataFrame(data_list)
    df.columns = ["id", "order_id", "order_date", "ship_date", "ship_mode", "customer_id", "customer_name", "segment", "city", "state", "country", "postal_code", "market", "region", "product_id", "category", "sub_category", "product_name", "sales", "quantity", "discount", "profit", "shipping_cost", "order_priority"]

    df['order_date'] = pd.to_datetime(df.order_date)

    warnings.filterwarnings("ignore")

    matplotlib.rcParams['axes.labelsize'] = 14
    matplotlib.rcParams['xtick.labelsize'] = 12
    matplotlib.rcParams['ytick.labelsize'] = 12
    matplotlib.rcParams['text.color'] = 'k'

    furniture = df.loc[df['category'] == 'Furniture']
    furniture['order_date'].min()
    furniture['order_date'].max()

    cols = ['id', 'order_id', 'ship_date', 'ship_mode', 'customer_id', 'customer_name', 'segment', 'country', 'city', 'state', 'postal_code', 'region', 'product_id', 'category', 'sub_category', 'product_name', 'quantity', 'discount', 'profit']

    furniture.drop(cols, axis=1, inplace=True)
    furniture = furniture.sort_values('order_date')
    furniture.isnull().sum()
    furniture = furniture.groupby('order_date')['sales'].sum().reset_index()
    furniture = furniture.set_index(furniture['order_date'])
    furniture.index
    y = furniture['sales'].resample('MS').mean()
    y.plot(figsize=(10, 6))

    img1 = io.BytesIO()
    plt.savefig(img1, format = 'png')
    img1.seek(0)
    plot1 = base64.b64encode(img1.getvalue()).decode()

    x = np.linspace(0, 1, 500)
    y = np.sin(4 * np.pi * x) * np.exp(-5 * x)
    fig, ax = plt.subplots()
    ax.fill(x, y, zorder=10)
    ax.grid(True, zorder=5)

    img2 = io.BytesIO()
    plt.savefig(img2, format = 'png')
    img2.seek(0)
    plot2 = base64.b64encode(img2.getvalue()).decode()

    x = np.linspace(0, 10, 500)
    dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off
    fig, ax = plt.subplots()
    line1, = ax.plot(x, np.sin(x), '--', linewidth=2, label='Dashes set retroactively')
    line1.set_dashes(dashes)
    line2, = ax.plot(x, -1 * np.sin(x), dashes=[30, 5, 10, 5], label='Dashes set proactively')
    ax.legend(loc='lower right')
    
    img3 = io.BytesIO()
    plt.savefig(img3, format = 'png')
    img3.seek(0)
    plot3 = base64.b64encode(img3.getvalue()).decode()

    if state:
        return jsonify({
            'text1': text1,
            'text2': text2,
            'plot1': plot1,
            'text3': text3,
            'plot2': plot2,
            'text4': text4,
            'plot3': plot3
        })
    else:
        return jsonify({'error': 'Missing data!'})

@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about-us")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')
        else:    
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account-info", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated.', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title="Update Post", form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))

@app.route("/download-guide")
def guide():
    return render_template('guide.html')






