import polars as pl
import requests
import yaml
from datetime import datetime
from flask import jsonify
from pathlib import Path


class TruelayerRaw:
    def __init__(self, bearer_token: str | None = None):
        self.bearer_token = bearer_token
        for attribute_name, attribute_value in load_truelayer_metadata().items():
            setattr(self, attribute_name, attribute_value)

    @property
    def access_link(self):
        return (
            f"{self.AUTH_URL}/?response_type=code&"
            f"client_id={self.CLIENT_ID}&scope={'%20'.join(self.scopes)}&"
            f"redirect_uri={self.REDIRECT_URI}&response_mode=query&"
            f"providers={'%20'.join(['uk-ob-'+provider for provider in self.providers])}"
        )


class TruelayerAPI(TruelayerRaw):
    def __init__(self, bearer_token: str):
        super().__init__(bearer_token)
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

def load_truelayer_metadata() -> dict:
    """Load the truelayer_metadata.yaml located next to this module and return it as a dict.

    Returns an empty dict if the file does not exist or cannot be parsed.
    """
    yaml_path = Path(__file__).parent / "truelayer_metadata.yaml"

    with yaml_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
        return data or {}

