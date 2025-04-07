import os
from typing import Annotated, Any, Dict, List

from dotenv import load_dotenv
from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from tronpy import Tron
from tronpy.exceptions import BadAddress
from tronpy.providers import HTTPProvider

from app.database import engine
from app.models import Wallet


load_dotenv()
router = APIRouter()

client = Tron(HTTPProvider(api_key=os.getenv("API_KEY")))


class WalletOut(BaseModel):
    address: str
    balance: int
    bandwidth: int
    energy: dict


@router.get("/api/v1/wallets", response_model=List[WalletOut | Dict[str, int]])
def get_wallets(
    page: int = Query(ge=0, default=0), size: int = Query(ge=1, le=100)
) -> Any:
    """
    Эндпоинт для получения всех записей из БД о кошельках.

    :param page: Параметр для пагинации - страница.
    :param size: Параметр для пагинации - кол-во кошельков на странице.
    :return:     Список кошельков.
    """
    offset_min = page * size
    offset_max = (page + 1) * size
    with Session(engine) as session:
        try:
            wallets = session.query(Wallet).all()
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Error: {e}")
    response = wallets[offset_min:offset_max] + [
        {
            "page": page,
            "size": size,
            "max_page": round(len(wallets) / size - 1, 0)
         }
    ]
    if not wallets:
        response = []
    return response


@router.post("/api/v1/balance", response_model=WalletOut)
def wallet_balance(address: Annotated[str, Body(embed=True)]) -> Any:
    """
    Эндпоинт на запрос данных о кошельке и записи данных в БД.

    :param address: Адрес кошелька.
    :return:        Данные о кошельке.
    """
    try:
        balance = client.get_account_balance(address)
        bandwidth = client.get_bandwidth(address)
        energy = client.get_account_resource(address)
    except BadAddress:
        raise HTTPException(status_code=422, detail="Address is invalid")
    with Session(engine) as session:
        wallet = Wallet(
            address=address,
            bandwidth=bandwidth,
            balance=int(balance),
            energy=energy,
        )
        try:
            session.add(wallet)
            session.commit()
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Error: {e}")
    return {
        "address": address,
        "balance": int(balance),
        "bandwidth": bandwidth,
        "energy": energy,
    }
