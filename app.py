import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json

import web3transactions as web3tx

import web3smartcontracts as contracts


with open("info.json", "r") as c:
    parameters = json.load(c)["parameters"]


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = parameters["database"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parameters["track_modifications"]
app.config['SECRET_KEY'] = parameters["secret_key"] 
app.config['UPLOAD_FOLDER'] = parameters["UPLOAD_FOLDER"]
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


class Blockkey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addres_key = db.Column(db.String(512), nullable=False)
    private_key = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return self.addres_key
    

class BlockUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addres_key = db.Column(db.String(512), nullable=False)
    private_key = db.Column(db.String(512), nullable=False)
    user_name = db.Column(db.String(512), nullable=False)
    user_password = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return self.addres_key + self.user_name


class BlockNfts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addres_key = db.Column(db.String(512), nullable=False)
    addres_location = db.Column(db.String(512), nullable=False)
    user_name = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return self.addres_key + self.user_name


class BlockOpen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addres_key = db.Column(db.String(512), nullable=False)
    problem_desc = db.Column(db.Text(), nullable=False)
    title_desc = db.Column(db.String(512), nullable=False)
    target_required = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.addres_key + " " + self.title_desc


@login_manager.user_loader
def load_user(id):
    return BlockUser.query.get(int(id))



# rough code to create blockkey
# @app.route('/', methods = ['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         addres_key = request.form.get('addres_key')
#         private_key = request.form.get('private_key')
#         block = Blockkey(addres_key = addres_key, private_key = private_key )
#         db.session.add(block)
#         db.session.commit()
#     blocks = Blockkey.query.all()
#     return render_template('index.html', blocks = blocks)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = request.form.get('amount')
        amount_sell = request.form.get('amount_sell')

        if amount:
            current_value = contracts.buy_coinvalue(int(amount))
            return render_template('test.html', current_value = current_value)

        if amount_sell:
            current_value = contracts.sell_coinvalue(int(amount_sell))
            return render_template('test.html', current_value = current_value)

    return render_template('test.html', current_value = contracts.retrievevalue())


@app.route('/nfts', methods = ['GET', 'POST'])
@login_required
def nfts():
    if request.method == 'POST':
        content = request.files['file']
        filename = secure_filename(content.filename)
        content.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        blocknft = BlockNfts(addres_key = current_user.addres_key, addres_location = str(os.path.join(app.config['UPLOAD_FOLDER'], filename)), user_name = current_user.user_name )
        db.session.add(blocknft)
        db.session.commit()

    blocks = BlockNfts.query.all()
    return render_template('nfts.html', blocks = blocks)


@app.route('/crowsourcing', methods = ['GET', 'POST'])
@login_required
def crowdsourcing():
    if request.method == 'POST':
        problem_desc = request.form.get('problem_desc')
        title_desc = request.form.get('title_desc')
        target_required = request.form.get('target_required')
        crowd = BlockOpen(addres_key = current_user.addres_key, problem_desc = problem_desc, title_desc = title_desc, target_required = int(target_required))
        db.session.add(crowd)
        db.session.commit()

    crowd = BlockOpen.query.all()
    return render_template('nfts.html', crowd = crowd)


@app.route('/makepayment', methods = ['GET', 'POST'])
@login_required
def makepayment():
    if request.method == 'POST':
        account_reciver = request.form.get('account_reciver')
        private_key_value = request.form.get('private_key')
        value = request.form.get('value')
        remark = request.form.get('remark')
        gas = 2000000

        if remark:
            crowd = BlockOpen.query.all()[0]
            crowd.target_required = crowd.target_required - int(value)
            db.session.commit()

        if private_key_value == current_user.private_key:
            hash_returned = web3tx.make_transaction(current_user.addres_key, account_reciver, current_user.private_key, value, gas)
            return redirect("http://localhost:3000/Dapp")
            # return render_template('index.html', user = current_user, hash_returned = hash_returned)

    return render_template('index.html', user = current_user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        print(user_name)
        print(user_password)
        pos_users = BlockUser.query.filter_by(user_name = user_name)

        for i in pos_users:
            if i.user_name == user_name and i.user_password == user_password:
                blockUser = BlockUser.query.get(i.id)
                load_user(blockUser.id)
                login_user(blockUser)
                return redirect(url_for('makepayment'))

    return render_template('login.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        blockkey = Blockkey.query.all()[0]
        blockUser = BlockUser(addres_key = blockkey.addres_key, private_key = blockkey.private_key, user_name = user_name, user_password = user_password)
        block_remove = Blockkey.query.get_or_404(blockkey.id)
        db.session.delete(block_remove)
        db.session.add(blockUser)
        db.session.commit()
        return redirect(url_for('login'))

    blocks = Blockkey.query.all()
    return render_template('login.html', blocks = blocks)


if __name__ == '__main__':
    app.run(debug = True, threaded = True)