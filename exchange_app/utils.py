import aiohttp


async def get_currencies():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.exchangerate-api.com/v4/latest/USD") as resp:
            result = await resp.json()
            return result.get("rates")