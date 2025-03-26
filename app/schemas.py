from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WalletInfo(BaseModel):
    address: str
    bandwidth: Optional[int] = Field(None)
    energy: Optional[int] = Field(None)
    trx_balance: Optional[int] = Field(None)
    
    class Config:
        from_attributes = True

class WalletQueryCreate(BaseModel):
    wallet_address: str

class WalletQueryResponse(WalletInfo):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: list[WalletQueryResponse]