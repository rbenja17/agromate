import logging
import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AgrofyMarketScraper:
    """Scraper for Agrofy News market data (Granos)."""
    
    URL = "https://news.agrofy.com.ar/granos"
    
    # Mapping of commodity names to our internal keys
    MAPPING = {
        "Soja": "soja",
        "Maíz": "maiz",
        "Trigo": "trigo",
        "Girasol": "girasol"
    }

    @classmethod
    async def get_prices(cls) -> Dict[str, Any]:
        """
        Scrape Pizarra Rosario prices from Agrofy.
        """
        results = {}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(cls.URL)
                response.raise_for_status()
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # The structure is a table-like layout
            # We look for rows containing our target commodities AND "Pizarra" AND "Rosario"
            
            # Note: This selector strategy is based on the provided text structure. 
            # Real HTML structure might vary, so we'll look for specific text containers.
            # Usually tables or card grids.
            
            # Implementation strategy: Find rows/cards
            rows = soup.find_all('tr') # Assuming standard table
            
            if not rows:
                 # Fallback: maybe it's not a table but a div grid. 
                 # Let's try to be generic or look for specific classes if we knew them.
                 # For now, let's assume standard table search or text based parsing if table fails.
                 pass

            # Since we don't know the exact HTML class names without seeing the source code, 
            # we will attempt a robust text-based search in the soup or standard table parsing.
            # Based on common Agrofy structure:
            
            tables = soup.find_all('table')
            for table in tables:
                for row in table.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    text_content = [c.get_text(strip=True) for c in cells]
                    
                    if not text_content:
                        continue
                        
                    # Target Format: [Grano, Mercado, Posición, Cotización, Variación, ...]
                    # Example: ['Soja', 'Pizarra', 'Rosario', '$ 470.000', '-1,26 %', ...]
                    
                    # Heurstic: Check if row has "Pizarra" and "Rosario"
                    row_text = " ".join(text_content).lower()
                    
                    if "pizarra" in row_text and "rosario" in row_text:
                        for commodity, key in cls.MAPPING.items():
                            if commodity.lower() in text_content[0].lower(): # First cell is usually Commodity Name
                                # Found a match!
                                # Price is usually in the 4th column (index 3) based on user example
                                # Soja | Pizarra | Rosario | $ 470.000
                                try:
                                    price_raw = text_content[3] # "$ 470.000"
                                    change_raw = text_content[4] # "-1,26 %"
                                    
                                    # Clean Price
                                    # "$ 470.000" -> 470000.0
                                    price_clean = price_raw.replace('$', '').replace('.', '').replace(',', '.').strip()
                                    price_val = float(price_clean)
                                    
                                    # Clean Change
                                    # "-1,26 %" -> -1.26
                                    change_clean = change_raw.replace('%', '').replace(',', '.').strip()
                                    change_val = float(change_clean)
                                    
                                    results[f"{key}_rosario"] = {
                                        "price": price_val,
                                        "currency": "ARS", # Pizarra Rosario is usually ARS
                                        "change_percent": change_val,
                                        "symbol": "Rosario",
                                        "name": f"{commodity} Rosario"
                                    }
                                except Exception as e:
                                    logger.warning(f"Error parsing row for {commodity}: {e}")

            # Fallback/Mock if scraping totally fails (for stability during dev)
            # if not results:
            #     return cls.get_mock_agrofy_data()
                
            return results

        except Exception as e:
            logger.error(f"Failed to scrape Agrofy: {e}")
            return {}
            
    @staticmethod
    def get_mock_agrofy_data():
        """Mock data matching Agrofy structure."""
        return {
            "soja_rosario": {"price": 470000, "currency": "ARS", "change_percent": -1.26, "symbol": "Rosario", "name": "Soja Rosario"},
            "maiz_rosario": {"price": 265000, "currency": "ARS", "change_percent": -3.01, "symbol": "Rosario", "name": "Maíz Rosario"},
            "trigo_rosario": {"price": 259560, "currency": "ARS", "change_percent": 0.28, "symbol": "Rosario", "name": "Trigo Rosario"},
            "girasol_rosario": {"price": 533540, "currency": "ARS", "change_percent": 0.28, "symbol": "Rosario", "name": "Girasol Rosario"}
        }
