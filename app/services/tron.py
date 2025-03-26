from datetime import datetime
from typing import Optional
from app.config import Settings
from app.utils.tron_client import initialize_tron_client
from app.utils.cache import cache_manager
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from app.schemas import WalletInfo
from app.api.errors import TronAPIError
import logging

logger = logging.getLogger(__name__)

class TronService:
    def __init__(self):
        self.client = initialize_tron_client()
        self._cache = cache_manager

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True
    )
    def _safe_api_call(self, method: callable, *args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            logger.warning(f"API call failed: {str(e)}")
            raise

    @cache_manager.cached()
    def get_wallet_info(self, address: str) -> WalletInfo:
        try:
            account = self._safe_api_call(self.client.get_account, address)
            balance = self._safe_api_call(self.client.get_account_balance, address)
            
            return WalletInfo(
                address=address,
                bandwidth=account.get("free_net_usage", None),
                energy=account.get("account_resource", {}).get("energy_usage", None),
                trx_balance=balance if balance is not None else None
            )
        except Exception as e:
            logger.error(f"Tron API error for {address}: {str(e)}")
            raise TronAPIError(f"API request failed: {str(e)}")

    def get_multiple_wallets(self, addresses: list[str]) -> dict[str, Optional[WalletInfo]]:
        results = {}
        uncached_addresses = []

        for addr in addresses:
            cache_key = f"wallet_info:{addr}"
            cached = self._cache._cache_store.get(cache_key)
            if cached and datetime.now() < cached['expires_at']:
                results[addr] = cached['value']
            else:
                uncached_addresses.append(addr)
        for addr in uncached_addresses:
            try:
                results[addr] = self.get_wallet_info(addr)
            except TronAPIError as e:
                results[addr] = None
                logger.warning(f"Skipped address {addr} due to error: {str(e)}")
        
        return results

    def clear_cache(self):
        self._cache.clear_cache()