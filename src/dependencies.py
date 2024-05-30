from src.redis import get_by_key


async def get_package_from_cache(package_name: str):
    key = "package_" + package_name.strip()
    return await get_by_key(key)


async def get_search_from_cache(q: str):
    key = "search_" + q.strip()
    return await get_by_key(key)
