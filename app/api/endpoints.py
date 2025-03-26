from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas import WalletQueryCreate, WalletQueryResponse, PaginatedResponse
from app.services.tron import TronService
from app.repositories.wallet import WalletRepository
from app.api.dependencies import get_db
from app.api.errors import InvalidRequestError, handle_app_errors

router = APIRouter()

@router.post("/wallet-info/", response_model=WalletQueryResponse)
@handle_app_errors
async def get_wallet_info(
    request: Request,
    wallet: WalletQueryCreate, 
    db: Session = Depends(get_db)
):
    tron_service = TronService()
    wallet_repo = WalletRepository(db)
    
    wallet_info = tron_service.get_wallet_info(wallet.wallet_address)
    db_query = wallet_repo.create_wallet_query(wallet_info)
    
    return WalletQueryResponse(
        address=db_query.address,
        bandwidth=db_query.bandwidth,
        energy=db_query.energy,
        trx_balance=db_query.trx_balance,
        id=db_query.id,
        created_at=db_query.created_at
    )

@router.get("/query-history/", response_model=PaginatedResponse)
@handle_app_errors
async def get_query_history(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db)
):
    wallet_repo = WalletRepository(db)
    
    if page < 1 or per_page < 1:
        raise InvalidRequestError("Page and per_page must be positive integers")
    
    skip = (page - 1) * per_page
    queries = wallet_repo.get_wallet_queries(skip, per_page)
    total = wallet_repo.get_total_queries_count()
    
    return PaginatedResponse(
        total=total,
        page=page,
        per_page=per_page,
        items=queries
    )