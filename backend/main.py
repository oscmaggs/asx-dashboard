from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/stocks/{ticker}")
def get_stock(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "name": info.get("longName"),
        "price": info.get("currentPrice"),
        "currency": info.get("currency"),
        "sector": info.get("sector"),
        "market_cap": info.get("marketCap"),
    }