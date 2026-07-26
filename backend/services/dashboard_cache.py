import time

_dashboard_cache = {}

CACHE_TIME = 30  # seconds


def get_cached_dashboard(user_id):
    data = _dashboard_cache.get(user_id)

    if not data:
        return None

    timestamp, dashboard = data

    if time.time() - timestamp > CACHE_TIME:
        del _dashboard_cache[user_id]
        return None

    return dashboard


def set_cached_dashboard(user_id, dashboard):
    _dashboard_cache[user_id] = (
        time.time(),
        dashboard
    )
