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
console docs:
https://docs.truelayer.com/docs/generate-an-auth-link#generating-an-auth-link

"""



import os
import requests
from flask import Flask, redirect, request, session, jsonify
from Kraken.accounting.accounts import Accounts

app = Flask(__name__)
app.secret_key = "dev"
app.my_global = {}

global_account = None

@app.route("/")
def home():

    auth_link = (
        f"{AUTH_URL}/?response_type=code&"
        f"client_id={CLIENT_ID}&scope={'%20'.join(scopes)}&"
        f"redirect_uri={REDIRECT_URI}&response_mode=query&providers=uk-ob-barclays%20uk-oauth-all"
    )
    auth_link = "https://auth.truelayer.com/?response_type=code&client_id=personalaccounting-9d862a&scope=info%20accounts%20balance%20cards%20standing_orders%20offline_access%20transactions%20direct_debits&redirect_uri=http://localhost:3000/callback&providers=uk-ob-barclays%20uk-ob-lloyds%20uk-ob-tesco%20uk-ob-capital-one%20uk-oauth-all"
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
    app.my_global["account"] = Accounts(bearer_token=token_data["access_token"])
    return redirect("accounts")

@app.route("/accounts", methods=["GET", "POST"])
def accounts():
    account_api = app.my_global.get("account")
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


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
