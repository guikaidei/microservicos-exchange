from fastapi import FastAPI, HTTPException
from uuid import uuid5, NAMESPACE_DNS
import httpx
from datetime import datetime

app = FastAPI()

API_URL = "https://economia.awesomeapi.com.br/json/last"

@app.get("/exchange/{from_currency}/{to_currency}")
async def get_exchange_rate(from_currency: str, to_currency: str):
    pair = f"{from_currency.upper()}-{to_currency.upper()}"
    url = f"{API_URL}/{pair}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch exchange rates")

    data = response.json()
    key = f"{from_currency.upper()}{to_currency.upper()}"

    if key not in data:
        raise HTTPException(status_code=404, detail="Currency pair not found")

    exchange = data[key]

    return {
        "sell": float(exchange["ask"]),
        "buy": float(exchange["bid"]),
        "date": exchange["create_date"],
        "id-account": str(uuid5(NAMESPACE_DNS, f"{from_currency}-{to_currency}-{exchange['timestamp']}"))
    }
