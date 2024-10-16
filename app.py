import yfinance as yf
import pandas as pd
from fastapi import FastAPI
import numpy as np
import datetime




app = FastAPI()

@app.get("/")
async def test():
     return {"message": "Share Calcultor api working fine"}


@app.get("/stock/monthly/{ticker}")
async def get_stock_data_monthly(ticker: str):

    ticker = yf.Ticker(ticker)
    daily_data = ticker.history(start="1996-01-01") 
    clean_data = daily_data.dropna(subset=['Open', 'High', 'Low', 'Close'])

    clean_data.index = pd.to_datetime(daily_data.index)

    pd.set_option('display.float_format', '{:.6f}'.format)

    monthly_data = daily_data.resample('ME').agg({
    'Open': 'first',   # First opening price of the month
    'High': 'max',     # Maximum high price of the month
    'Low': 'min',      # Minimum low price of the month
    'Close': 'last',   # Last closing price of the month
    'Volume': 'sum'    # Total volume for the month
    })

    monthly_data.replace([np.inf, -np.inf], None, inplace=True)  # Replace infinities with None
    monthly_data.where(pd.notnull(monthly_data), None, inplace=True)  # Replace NaNs with None

    # Convert monthly data to a list of dictionaries
    monthly_data_list = monthly_data.reset_index().to_dict(orient='records')

    return {"message": "Monthly Data fetched successfully", "data": monthly_data_list}

# Get Daily data
@app.get("/stock/daily/{ticker}")
async def get_stock_data_daily(ticker: str):

    ticker = yf.Ticker(ticker)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    daily_data = ticker.history(start=f"{year}-{month}-01") 
    clean_data = daily_data.dropna(subset=['Open', 'High', 'Low', 'Close'])

    clean_data.index = pd.to_datetime(daily_data.index)

    pd.set_option('display.float_format', '{:.6f}'.format)

   

    daily_data.replace([np.inf, -np.inf], None, inplace=True)  # Replace infinities with None
    daily_data.where(pd.notnull(daily_data), None, inplace=True)  # Replace NaNs with None

    # Convert monthly data to a list of dictionaries
    daily_data_list = daily_data.reset_index().to_dict(orient='records')

    return {"message": "Daily Data fetched successfully", "data": daily_data_list}
   


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)