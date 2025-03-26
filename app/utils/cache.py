from functools import wraps
from datetime import datetime, timedelta
from typing import Callable, Optional, TypeVar, Any
import hashlib
import pickle
from app.config import settings
import logging
import inspect

logger = logging.getLogger(__name__)
T = TypeVar('T')

class CacheManager:
    _instance = None
    _cache_store = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._setup_cache()
        return cls._instance
    
    @classmethod
    def _setup_cache(cls):
        cls._cache_store = {}
        logger.info("Cache initialized")
    
    @staticmethod
    def _generate_key(func: Callable, *args, **kwargs) -> str:
        if args and inspect.ismethod(func):
            args = args[1:]  
        
        try:
            args_str = pickle.dumps((args, kwargs))
        except (pickle.PicklingError, TypeError):
            args_str = f"{args!r}:{kwargs!r}".encode('utf-8')
        
        return f"{func.__module__}.{func.__name__}:{hashlib.md5(args_str).hexdigest()}"
    
    def cached(
        self, 
        ttl: int = 300, 
        max_size: int = 1000,
        key_prefix: Optional[str] = None,
        ignore_self: bool = True  
    ) -> Callable[[Callable[..., T]], Callable[..., T]]:
        
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                if not settings.CACHE_ENABLED:
                    return func(*args, **kwargs)

                if ignore_self and args and inspect.ismethod(func):
                    cache_args = args[1:]
                else:
                    cache_args = args
                
                cache_key = key_prefix or self._generate_key(func, *cache_args, **kwargs)

                if cache_key in self._cache_store:
                    entry = self._cache_store[cache_key]
                    if datetime.now() < entry['expires_at']:
                        logger.debug(f"Cache hit for {cache_key}")
                        return entry['value']
                    del self._cache_store[cache_key]

                result = func(*args, **kwargs)

                if len(self._cache_store) < max_size:
                    self._cache_store[cache_key] = {
                        'value': result,
                        'expires_at': datetime.now() + timedelta(seconds=ttl)
                    }
                    logger.debug(f"Cached result for {cache_key} (TTL: {ttl}s)")
                
                return result
            
            return wrapper
        return decorator
    
    def clear_cache(self):
        self._cache_store.clear()
        logger.info("Cache cleared")

cache_manager = CacheManager()