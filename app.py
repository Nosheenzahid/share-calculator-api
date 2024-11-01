import yfinance as yf
from fastapi import FastAPI
from typing import Optional
from datetime import date
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

class StockRequest(BaseModel):
    ticker: str

class StockData(BaseModel):
    symbol: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    error: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

@app.get("/")
async def test():
    return {"message": "Share Calculator API working fine"}

@app.post("/stock/all")
async def get_all_stock_data(stock_request: StockRequest):
    tickers_data = {}
    ticker_string = stock_request.ticker.strip()
    all_tickers_data = yf.Tickers(ticker_string)
    tickers = ticker_string.split()

    def fetch_ticker_data(ticker):
        try:
            data = all_tickers_data.tickers[ticker].history(period="1d")
            data_dict = data.reset_index().to_dict(orient='records')
            return ticker, data_dict
        except Exception as e:
            return ticker, {"error": str(e)}

    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_ticker_data, tickers)

    for ticker, data_dict in results:
        tickers_data[ticker] = data_dict

    
    return {"message": "Daily Data fetched successfully", "data": tickers_data}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
