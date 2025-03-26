import logging
from fastapi import HTTPException, status, Request
from functools import wraps
from typing import Callable, Any
import traceback

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Базовый класс для ошибок приложения"""
    pass

class TronAPIError(AppError):
    """Ошибка при обращении к Tron API"""
    pass

class DatabaseError(AppError):
    """Ошибка работы с базой данных"""
    pass

class InvalidRequestError(AppError):
    """Некорректный запрос"""
    pass

class WalletNotFoundError(AppError):
    """Кошелек не найден"""
    pass

def handle_app_errors(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
        try:
            logger.debug(f"Handling request: {request.method} {request.url.path}")
            return await func(request, *args, **kwargs)
            
        except InvalidRequestError as e:
            logger.warning(f"Invalid request to {request.url.path}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
            
        except WalletNotFoundError as e:
            logger.warning(f"Wallet not found at {request.url.path}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
            
        except TronAPIError as e:
            logger.error(f"Tron API error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="API request failed"
            )
            
        except DatabaseError as e:
            logger.error(f"Database error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
            
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
            
    return wrapper