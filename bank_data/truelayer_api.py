import polars as pl
import requests
from datetime import datetime
from flask import jsonify
from pathlib import Path


class TruelayerRaw:
    CLIENT_ID = "personalaccounting-9d862a"
    CLIENT_SECRET = "7c35e5c4-86b2-4035-9970-331f182c0974"
    REDIRECT_URI= "http://localhost:3000/callback"
    AUTH_URL="https://auth.truelayer.com"
    API_URL="https://api.truelayer.com"
    scopes = [
        "info", "accounts", "balance", "cards", "transactions",
        "direct_debits", "standing_orders", "offline_access"
    ]
    providers = [
        "barclays",
        "lloyds",
        "tesco",
        "capital-one"
    ]

    @property
    def access_link(self):
        auth_link = "https://auth.truelayer.com/?response_type=code&client_id=personalaccounting-9d862a&scope=info%20accounts%20balance%20cards%20standing_orders%20offline_access%20transactions%20direct_debits&redirect_uri=http://localhost:3000/callback&providers=uk-ob-barclays%20uk-ob-lloyds%20uk-ob-tesco%20uk-ob-capital-one%20uk-oauth-all"

        return (
            f"{self.AUTH_URL}/?response_type=code&"
            f"client_id={self.CLIENT_ID}&scope={'%20'.join(self.scopes)}&"
            f"redirect_uri={self.REDIRECT_URI}&response_mode=query&"
            f"providers={'%20'.join(['uk-ob-'+provider for provider in self.providers])}"
        )


class TruelayerAPI(TruelayerRaw):
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self._accounts_request = self.get_accounts()

    def get_accounts(self):
        accounts_get_request = requests.get(
            f"{self.API_URL}/data/v1/accounts", 
            headers={"Authorization": f"Bearer {self.bearer_token}"}
        )
        if accounts_get_request.status_code != 200:
            return f"Error fetching transactions: {accounts_get_request.text} {accounts_get_request.status_code}"
        return accounts_get_request.json()
    
    @property
    def account_ids(self):
        return [
            account["account_id"] 
            for account in self._accounts_request["results"]
        ]
    
    def save_accounts(self):
        current_date = datetime.now().date().strftime("%Y-%m-%d")
        path = f"/raw_data/retrievers/bank_data/bank_accounts/{current_date}"
        print(f"Saving accounts in {path}")

        output_dir = Path(path)
        output_dir.mkdir(parents=True, exist_ok=True)

        pl.DataFrame(self._accounts_request["results"]).with_columns(
            pl.lit(self._accounts_request["status"]).alias("status"),
            pl.col("update_timestamp").str.strptime(pl.Datetime).dt.convert_time_zone("Europe/London").alias("updatetime")
        ).to_pandas().to_parquet(
            f"{output_dir}/accounts.parquet"
        )

    def transactions(self, account_id):
        transactions_get_request = requests.get(
            f"{self.API_URL}/data/v1/accounts/{account_id}/transactions",
            headers={"Authorization": f"Bearer {self.bearer_token}"}
        )
        if transactions_get_request.status_code != 200:
            return f"Error fetching transactions: {transactions_get_request.text} {transactions_get_request.status_code}"
        transactions =  jsonify(transactions_get_request.json()).json
        return pl.DataFrame(transactions["results"]).with_columns(
            pl.lit(transactions["status"]).alias("status"),
            pl.lit(account_id).alias("account_id"),
            pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%SZ").alias("timestamp"),
        )
    
    def save_transactions(self, account_id):
        

        current_date = datetime.now().date().strftime("%Y-%m-%d")

        path = f"/raw_data/retrievers/bank_data/bank_transactions/{current_date}"
        print(f"Saving transactions for account {account_id} in {path}")

        output_dir = Path(path)
        output_dir.mkdir(parents=True, exist_ok=True)

        self.transactions(account_id).to_pandas().to_parquet(
            f"{output_dir}/{account_id}.parquet"
        )
