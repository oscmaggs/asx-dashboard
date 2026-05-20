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

@app.get("/api/stocks/{ticker}/history")
def get_stock_history(ticker: str, days: int = 30):
    if days < 1 or days > 3650:
        raise HTTPException(
            status_code=400,
            detail=f"Days must be between 1 and 3650"
        )
    
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=f"{days}d")
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch history for '{ticker}'"
        )

    if history.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No history found for '{ticker}'"
        )

    records = [
        {
            # %y is 4 digits, %m is 2 digits %d is 2 digits makes format like 2026-05-20
            "date": index.strftime("%Y-%m-%d"),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        }
        for index, row in history.iterrows()
    ]

    return {
        "ticker": ticker,
        "days": days,
        "count": len(records),
        "history": records,
    }