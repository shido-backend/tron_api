from tronpy import Tron
from tronpy.providers import HTTPProvider
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def initialize_tron_client(network: str = None) -> Tron:
    try:
        network = network or settings.tron_network
        provider_url = (
            "https://api.trongrid.io" 
            if network == "mainnet" 
            else "https://api.shasta.trongrid.io"
        )
        
        logger.debug(f"Initializing Tron client for {network} network")
        return Tron(HTTPProvider(provider_url))
        
    except Exception as e:
        logger.error(f"Failed to initialize Tron client: {str(e)}")
        raise ValueError(f"Tron client initialization failed: {str(e)}")