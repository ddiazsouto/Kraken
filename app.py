import requests
import secrets
from flask import Flask, redirect, render_template, request

from bank_data.truelayer_api import TruelayerAPI, TruelayerRaw
from bank_data.functions.remaining_direct_debits_logic import remaining_direct_debits_logic
from formularium import login_form, body_composition, add_gym_data_selection, updating

from user import User


app = Flask(__name__, template_folder='frontend/templates')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.my_global = {
    "access_key": secrets.token_hex(16)
}

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


@app.route("/callback", methods=["GET", "POST"])
def callback():

    code = request.args.get("code")
    if not code:
        return "No code in callback."
    
    truelayer_data = TruelayerRaw()
    _data = {
        "grant_type": "authorization_code",
        "client_id": truelayer_data.CLIENT_ID,
        "client_secret": truelayer_data.CLIENT_SECRET,
        "redirect_uri": truelayer_data.REDIRECT_URI,
        "scope": request.args.get("scope"),
        "code": code 
    }
    token_resp = requests.post(
        f"{truelayer_data.AUTH_URL}/connect/token", data=_data
    )

    if token_resp.status_code != 200:
        return f"Error fetching token: {token_resp.text}", 500

    token_data = token_resp.json()
    truelayer_api = TruelayerAPI(bearer_token=token_data["access_token"])
    truelayer_api.save_accounts()
    for account_id in truelayer_api.account_ids:
        truelayer_api.save_transactions(account_id)

    app.my_global["truelayer_api"] = truelayer_api

    return redirect("calculate_remaining_transactions")


@app.route("/calculate_remaining_transactions", methods=["GET", "POST"])
def accounts():
    truelayer_api = app.my_global.get("truelayer_api")
    direct_debits_account  = "e0abf34cb5ad739813add80fb5aa99c4"
    new_transactions_df = truelayer_api.transactions(
        direct_debits_account
    ).select(
        "description", "amount", "timestamp"
    )
    returned_df = remaining_direct_debits_logic(new_transactions_df)

    return f"<html><head></head> <body>Remaining amount: {sum(returned_df['amount'].to_list())},<br><hr> From: <br>{'<br>'.join(returned_df['description'].to_list())}</body></html>"




@app.route('/master_home')
def sales():

    user=User()
    list=[]

    if request.method=='GET':
        pass        

    return render_template('master_home.html', title='Sales', user=user, list=list)



@app.route('/reports', methods=['GET', 'POST'])
def Master():

    user=User()

    return render_template('master.html', title='Master', user=user)



"""
    Here the app runs       and lives       not to touch        leave alone     logic above
"""


if __name__=='__main__':
    app.run(debug=True, port=3000, host="0.0.0.0")

# MySQL.off()
