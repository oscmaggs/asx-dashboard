from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/stocks/{ticker}")
def get_stock(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch data for '{ticker}' from upstream"
        )
    if not info or not info.get("longName"):
        raise HTTPException(
            status_code=404,
            detail=f"Stock ticker: '{ticker}' not found"
        )


    return {
        "ticker": ticker,
        "name": info.get("longName"),
        "price": info.get("currentPrice"),
        "currency": info.get("currency"),
        "sector": info.get("sector"),
        "market_cap": info.get("marketCap"),
    }