from sqlalchemy.orm import Session
from app.models import WalletQuery
from app.schemas import WalletInfo
from app.api.errors import DatabaseError
import logging

logger = logging.getLogger(__name__)

class WalletRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_wallet_query(self, wallet_info: WalletInfo) -> WalletQuery:
        try:
            db_query = WalletQuery(
                address=wallet_info.address,
                bandwidth=wallet_info.bandwidth,
                energy=wallet_info.energy,
                trx_balance=wallet_info.trx_balance
            )
            self.db.add(db_query)
            self.db.commit()
            self.db.refresh(db_query)
            return db_query
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database error when creating wallet query: {str(e)}")
            raise DatabaseError("Failed to create wallet record")

    def get_wallet_queries(self, skip: int = 0, limit: int = 10) -> list[WalletQuery]:
        try:
            return self.db.query(WalletQuery)\
                    .order_by(WalletQuery.created_at.desc())\
                    .offset(skip)\
                    .limit(limit)\
                    .all()
        except Exception as e:
            logger.error(f"Database error when fetching queries: {str(e)}")
            raise DatabaseError("Failed to get wallet queries")

    def get_total_queries_count(self) -> int:
        try:
            return self.db.query(WalletQuery).count()
        except Exception as e:
            logger.error(f"Database error when counting queries: {str(e)}")
            raise DatabaseError("Failed to count wallet queries")