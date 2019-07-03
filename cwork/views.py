from flask import render_template, session, url_for, redirect, request
from .forms import RegistrationForm, InputSpendings
from .plotter import per_payee, per_month
from datetime import datetime
import bcrypt
from cwork import app, db
from pymongo import DESCENDING
from bson.objectid import ObjectId


@app.route("/index", methods=['POST', 'GET'])
def index():

    form = InputSpendings(request.form)

    if request.method == 'POST' and form.validate():
        spendings = db.spendings
        
        spendings.insert_one(
            {
                'author': session['username'],
                'contas': {
                    'month_ref': form['date_ref'].data.strftime('%Y-%m'),
                    'payee': form['payee'].data,
                    'amount': form['amount'].data
                }, 
                'created': datetime.now()
            }
        )

        plot = per_month(spendings)

        return redirect(url_for('index'))
    
    plot = per_month(db.spendings)

    return render_template(
        "index.html",
        name=session['username'],
        form=InputSpendings(), 
        table=db.spendings.find({}, limit=10).sort('contas.month_ref', DESCENDING),
        plot=plot,
        page_title = 'Dashboard'
        )
    
@app.route("/delete_entry", methods=['POST'])
def delete_entry():
    
    db.spendings.find_one_and_delete({"_id":ObjectId(request.form['_id'])})
    
    return redirect(url_for('index'))


@app.route("/login", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        users = db.users
        login_user = users.find_one({'email': request.form['email'] })

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = login_user['username']
                return redirect(url_for('index'))
            
        return render_template("login.html", error=True, page_title = 'Login')
    return render_template("login.html", page_title = 'Login')
    
@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        users = db.users
        existing_user = users.find_one( {'$or': [{'email': request.form['email']}, {'username': request.form['username']}]})

        if existing_user == None:
            hashpass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'email': request.form['email'], 'username': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return 'Username or email already registered, please log in'
    
    if request.method == 'POST' and not form.validate():
       return render_template('register.html', form=form, page_title = 'Register') 
    
    return render_template("register.html", form=form, page_title = 'Register')
