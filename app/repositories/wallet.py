from sqlalchemy import exc
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
        except exc.SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error: {str(e)}", exc_info=True)
            raise DatabaseError("Failed to create wallet record") from e

    def get_wallet_queries(self, skip: int = 0, limit: int = 10) -> list[WalletQuery]:
        try:
            return self.db.query(WalletQuery)\
                    .order_by(WalletQuery.created_at.desc())\
                    .offset(skip)\
                    .limit(limit)\
                    .all()
        except exc.SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}", exc_info=True)
            raise DatabaseError("Failed to fetch queries") from e

    def get_total_queries_count(self) -> int:
        try:
            return self.db.query(WalletQuery).count()
        except exc.SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}", exc_info=True)
            raise DatabaseError("Failed to count queries") from e