class Configuration:
    table = "_lonny_pg_lock"
    default_locker_name = "_default"
    stale_lock_seconds = 5 * 60
    dead_lock_days = 90