from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import (
    WalletQueryCreate, 
    WalletQueryResponse,
    PaginatedResponse
)
from app.services.tron import TronService, DatabaseService
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/wallet-info/", response_model=WalletQueryResponse)
async def get_wallet_info(
    wallet: WalletQueryCreate, 
    db: Session = Depends(get_db)
):
    try:
        tron_service = TronService()
        wallet_info = tron_service.get_wallet_info(wallet.wallet_address)
        db_query = DatabaseService.create_wallet_query(db, wallet_info)
        
        return WalletQueryResponse(
            address=db_query.address,
            bandwidth=db_query.bandwidth,
            energy=db_query.energy,
            trx_balance=db_query.trx_balance,
            id=db_query.id,
            created_at=db_query.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@router.get("/query-history/", response_model=PaginatedResponse)
async def get_query_history(
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1 or per_page < 1:
        raise HTTPException(
            status_code=400, 
            detail="Page and per_page must be positive integers"
        )
    
    skip = (page - 1) * per_page
    queries = DatabaseService.get_wallet_queries(db, skip, per_page)
    total = DatabaseService.get_total_queries(db)
    
    return PaginatedResponse(
        total=total,
        page=page,
        per_page=per_page,
        items=queries
    )