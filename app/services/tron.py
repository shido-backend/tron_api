from tronpy import Tron
from tronpy.providers import HTTPProvider
from app.config import settings
from app.models import WalletQuery
from app.schemas import WalletInfo
from sqlalchemy.orm import Session

class TronService:
    def __init__(self):
        network = settings.tron_network
        if network == "mainnet":
            self.client = Tron(HTTPProvider("https://api.trongrid.io"))
        else:
            self.client = Tron(HTTPProvider("https://api.shasta.trongrid.io"))

    def get_wallet_info(self, address: str) -> WalletInfo:
        try:
            account = self.client.get_account(address)
            balance = self.client.get_account_balance(address)
            
            return WalletInfo(
                address=address,
                bandwidth=account.get("free_net_usage", None),
                energy=account.get("account_resource", {}).get("energy_usage", None),
                trx_balance=balance if balance is not None else None
            )
        except Exception as e:
            return WalletInfo(
                address=address,
                bandwidth=None,
                energy=None,
                trx_balance=None
            )

class DatabaseService:
    @staticmethod
    def create_wallet_query(db: Session, wallet_info: WalletInfo) -> WalletQuery:
        db_query = WalletQuery(
            address=wallet_info.address,
            bandwidth=wallet_info.bandwidth,
            energy=wallet_info.energy,
            trx_balance=wallet_info.trx_balance
        )
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
        return db_query

    @staticmethod
    def get_wallet_queries(
        db: Session, 
        skip: int = 0, 
        limit: int = 10
    ) -> list[WalletQuery]:
        return db.query(WalletQuery)\
                .order_by(WalletQuery.created_at.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()

    @staticmethod
    def get_total_queries(db: Session) -> int:
        return db.query(WalletQuery).count()