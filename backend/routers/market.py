from fastapi import APIRouter
from services.market_data import MarketDataService

router = APIRouter(
    prefix="/api/market",
    tags=["market"]
)

@router.get("/latest")
async def get_market_data():
    """
    Get latest market prices for commodities.
    """
    # Use real data service
    data = MarketDataService.get_latest_prices()
    
    # Simple fallback check
    if "error" in data:
        return MarketDataService.get_mock_data()
        
    return data
