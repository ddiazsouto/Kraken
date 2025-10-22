import requests
import secrets
from flask import Flask, redirect, render_template, request

from accounting.truelayer_api import TruelayerAPI, TruelayerRaw
from formularium import login_form, body_composition, add_gym_data_selection, updating

from user import User


"""
Up here the app and database configuration are defined as well as their connections to python

First the connection the database through SQLAlchemy

"""

from flask import Flask


app = Flask(__name__, template_folder='frontend/templates')
app.config['SECRET_KEY']='dAnIel52'
app.my_global = {
    "access_key": secrets.token_hex(16)
}

CLIENT_ID = "personalaccounting-9d862a"
CLIENT_SECRET = "7c35e5c4-86b2-4035-9970-331f182c0974"
REDIRECT_URI= "http://localhost:3000/callback"
AUTH_URL="https://auth.truelayer.com"
API_URL="https://api.truelayer.com"
scopes = [
    "info", "accounts", "balance", "cards", "transactions",
    "direct_debits", "standing_orders", "offline_access"
]

"""
Now some logic for the app and its routes

"""


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')


log = "login"
@app.route(f'/{log}', methods=['GET', 'POST'])
def login():
    

    user = User()
    template='login.html'
    form = login_form()
    msg=""

    if request.method=='POST' and user.check(form.login.data, form.passwd.data):
        template = user.home_template
    elif request.method=='POST':
            msg='Please, wrong username or password'

    return render_template(
        template,
        title='Welcome',
        form=form,
        message=msg,
        user=user,
        truelayer_link=TruelayerRaw().access_link
    )


@app.route(
    '/add_body_composition',
    methods=['GET', 'POST']
)
def add_body_composition():

    user=User()
    editing=updating()
    msg = None


    # if request.method=='POST':
    #     data = body_composition()
        
    #     msg = True

    return render_template('client.html',
                           form3=editing,
                           message=msg,
                           select_input_type=add_gym_data_selection(),
                           form=body_composition(), user=user)

@app.route(
    '/accounting',
    methods=['GET', 'POST']
)
def access_truelayer():

    auth_link = (
        f"{AUTH_URL}/?response_type=code&"
        f"client_id={CLIENT_ID}&scope={'%20'.join(scopes)}&"
        f"redirect_uri={REDIRECT_URI}&response_mode=query&providers=uk-ob-barclays%20uk-oauth-all"
    )
    return f'<a href="{auth_link}">Refresh transactions</a>'



@app.route("/callback", methods=["GET", "POST"])
def callback():

    code = request.args.get("code")
    if not code:
        return "No code in callback."

    _data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "scope": request.args.get("scope"),
        "code": code 
    }
    token_resp = requests.post(f"{AUTH_URL}/connect/token", data=_data)

    if token_resp.status_code != 200:
        return f"Error fetching token: {token_resp.text}", 500

    token_data = token_resp.json()
    app.my_global["truelayer_api"] = TruelayerAPI(bearer_token=token_data["access_token"])
    return redirect("accounts")


@app.route("/accounts", methods=["GET", "POST"])
def accounts():
    account_api = app.my_global.get("truelayer_api")
    account_ids = account_api.account_ids

    account_api.save_accounts()
    for account_id in account_ids:
        account_api.save_transactions(account_id)

    # The following should be extracted in a different endpoint
    # for now we find it useful to return the pending direct debits, although
    # this should be a new option and endpoint
    from datetime import datetime, timedelta
    import polars as pl

    columns = [
        'amount', 'description', 'timestamp', 'payment_month'
    ]
    direct_debits = pl.read_delta(
        "/data_warehouse/data/bank_data/staging/bank_transactions",
        columns=['amount', 'description', 'expense', 'timestamp', 'payment_month']
    ).filter(
        (pl.col("payment_month") == 7) & (pl.col("expense").is_not_null())
    )
    new_transactions = account_api.transactions("e0abf34cb5ad739813add80fb5aa99c4").select(
        "description", "amount", "timestamp"
    ).with_columns(
            pl.when(pl.col("description").str.contains("AXA") | pl.col("description").str.contains("COSTA LIMITED"))
      .then((pl.lit("beginning")))
      .alias("temp_col")
    ).filter(
        pl.col("timestamp") > (datetime.now() - timedelta(days=30))
    )

    beginning = new_transactions.filter(
        pl.col("temp_col").is_in(["beginning"])
    ).sort("timestamp").head(1).select("timestamp").item()

    new_transactions = new_transactions.filter(
        pl.col("timestamp") > beginning
    )

    returned_df = direct_debits.join(
        new_transactions,
        on=pl.col("description").str.slice(0, 15),
        how="anti"
    )
    pl.Config(tbl_rows=300)
    return f"<html><head></head> <body>Remaining amount: {sum(returned_df['amount'].to_list())},<br><hr> From: <br>{'<br>'.join(returned_df['description'].to_list())}</body></html>"




@app.route('/master_home')
def sales():

    user=User()
    list=[]

    if request.method=='GET':
        pass        

    return render_template('master_home.html', title='Sales', user=user, list=list)



@app.route('/Over', methods=['GET', 'POST'])
def Master():

    user=User()

    return render_template('master.html', title='Master', user=user)



"""
    Here the app runs       and lives       not to touch        leave alone     logic above
"""


if __name__=='__main__':
    app.run(debug=True, port=3000, host="0.0.0.0")

# MySQL.off()
