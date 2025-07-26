import httpx
from core.config import BitConfig

async def create_bit_payment(amount: float, order_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BitConfig.API_URL}/create",
            headers={"Authorization": BitConfig.API_KEY},
            json={"amount": amount, "order_id": order_id}
        )
        return response.json()
