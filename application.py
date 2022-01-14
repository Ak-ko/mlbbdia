import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response
import json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from assistance import login_required



app = Flask(__name__)

# initialization the database
db = SQL('sqlite:///diamond.db')

app.config["TEMPLATES_AUTO_RELOAD"] = True

COINAMOUNT = [100,250,400,550,1000,2500]
COINPRICE = [100,250,400,550,1000,2500]


DIAPRICE = [50,150,300,450,700,1200,2000,3100,4800]
DIAAMOUNT = [40,120,201,423,808,1150,1900,2900,3900]

# for cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


### home ###
@app.route("/",methods=["GET","POST"])
# @app.route("/<string:coinBuy>")
@login_required
def index(coinBuy=None):

    users = session["user_id"]

    # getting the userid
    userids = db.execute('SELECT userid FROM userinfos WHERE id = ?', users)
    userid = userids[0]["userid"]

    # getting the zoneid
    zoneids = db.execute('SELECT zoneid FROM userinfos WHERE userid = ?', userid)
    zoneid = zoneids[0]["zoneid"]

    # coin amount
    coins = db.execute('SELECT coinamount FROM userinfos WHERE userid = ?', userid)
    coin_auto = coins[0]["coinamount"]

    diamondInDb = db.execute('SELECT diamondamount FROM userinfos WHERE userid = ?', userid)
    diamondDisplay = diamondInDb[0]['diamondamount']

    # getting the prices
    coins = db.execute('SELECT * FROM coins')
    diamonds = db.execute('SELECT * FROM diamonds')

    diamondjson = [
        {"amount":40, "price" : 50},
        {"amount":120, "price" : 150},
        {"amount":201, "price" : 300},
        {"amount":423, "price" : 450},
        {"amount":808, "price" : 700},
        {"amount":1150, "price" : 1200},
        {"amount":1900, "price" : 2000},
        {"amount":2900, "price" : 3100},
        {"amount":3900, "price" : 4800},
    ]

    # Select Diamonds from db
    diabuy = db.execute("SELECT diaamount FROM diamondbuy WHERE diabuyerid = ?", session["user_id"])



    coinjson = [
        {"amount" : 100, "price" : 100},
        {"amount" : 250, "price" : 250},
        {"amount" : 400, "price" : 400},
        {"amount" : 550, "price" : 550},
        {"amount" : 1000, "price" : 1000},
        {"amount" : 2500, "price" : 2500},
    ]

    usermoney = db.execute("SELECT bankmoney FROM userinfos WHERE id = ?", session["user_id"])

    bank = usermoney[0]["bankmoney"]

    bankmoney = [
        {
            "amount" : bank
        }
    ]


    # putting the coins into the database
    coinamount = 0
    coinprice = 0
    while coinamount < len(COINAMOUNT):
        while coinprice < len(COINPRICE):
            if len(coins) == 0:
                db.execute('INSERT INTO coins(coinamount,coinprice) VALUES (?,?)', COINAMOUNT[coinamount], COINPRICE[coinprice])
            coinprice += 1
            coinamount += 1
        coinamount = len(COINAMOUNT)

    # putting the diamonds into the database
    diaamount = 0
    diaprice = 0
    while diaamount < len(DIAAMOUNT):
        while diaprice < len(DIAPRICE):
            if len(diamonds) == 0:
                db.execute('INSERT INTO diamonds(diamondamount,diamondprice) VALUES (?,?)', DIAAMOUNT[diaamount], DIAPRICE[diaprice])
            diaprice += 1
            diaamount += 1
        diaamount = len(DIAAMOUNT)




    return render_template(
            'index.html',

            userid=userid,

            users=users,

            zoneid=zoneid,

            coin=coin_auto,

            coinprices=COINPRICE,

            coinjson = coinjson,

            diamonds=DIAAMOUNT,

            diamondbuy=diabuy,

            diamondjson=diamondjson,

            diamondDisplay=diamondDisplay,

            bankmoney=bankmoney
        )

@app.route('/process/<string:entry>',methods=['POST','GET'])
def process(entry):

    entryCoins = json.loads(entry)

    coins = entryCoins['coins']

    coinbought = entryCoins['coinbought']
    coinamount = coinbought

    currentUser = session["user_id"]

    db.execute('UPDATE userinfos SET coinamount = ? WHERE id = ?', coins, currentUser)

    db.execute('INSERT INTO coinbuy(buyerid,coinprice,coinamount) VALUES (?,?,?)', currentUser, coinbought, coinamount)
    return 'Purchase Successfull !'

@app.route('/diamonds/<string:diamond_entry>', methods=["POST","GET"])
def diamonds(diamond_entry):

    diamondsEntry = json.loads(diamond_entry);

    diaAmount = diamondsEntry['diamondAmount']

    diaPrice = diamondsEntry['diamondPrice']

    coinAfter = diamondsEntry['coinafter']

    currentUser = session["user_id"]


    db.execute("UPDATE userinfos SET coinamount = ? WHERE id = ?", coinAfter,currentUser)

    db.execute('INSERT INTO diamondbuy(diabuyerid, diaprice, diaamount) VALUES (?,?,?)', currentUser, diaPrice, diaAmount)

    db.execute('UPDATE userinfos SET diamondamount = ? WHERE id = ?', diaAmount, currentUser)
    return 'Operation Success!'


### login ###
@app.route('/login',methods=["GET", "POST"])
def login():
    # forget any previous user
    session.clear()

    if request.method == "POST":

        # get the details of a user

        if len(request.form.get("userid")) != 9:
            return render_template('error.html',status = "INVALID USERID",code = 406, message = "Sir, please provide valid your userid.")

        if len(request.form.get("zoneid")) != 4:
            return render_template('error.html',status="INVALID ZONEID",code=406,message="Sir, please provide valid your zoneid")

        rows = db.execute("SELECT * FROM userinfos WHERE userid = ?", request.form.get('userid'))


        if len(rows) != 1:
            ids = db.execute('INSERT INTO userinfos (userid,zoneid) VALUES (?,?)', request.form.get('userid'), request.form.get('zoneid'))

            #getting the user details again
            rows = db.execute("SELECT * FROM userinfos WHERE userid = ?", request.form.get('userid'))

            session["user_id"] = rows[0]["id"]
            return redirect('/')
        else:
            session["user_id"] = rows[0]["id"]
            return redirect('/')

        return redirect('/')
    else:
        return render_template("login.html")

### logout ###
@app.route("/logout")
def logout():

    #forget any users
    session.clear()

    return redirect('/')

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return e.name,e.code


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

