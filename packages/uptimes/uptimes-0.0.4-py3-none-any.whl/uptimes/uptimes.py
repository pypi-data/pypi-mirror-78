import datetime

start_time = datetime.datetime.now()  # Timestamp when it initializes.


def __init__():
    start_time = datetime.datetime.now()  # Timestamp when it initializes.


def uptimes():
    now = datetime.datetime.now()  # Timestamp when uptime function runs.
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    uptime_stamp = (
        f"**{days}** days **{hours}** hours **{minutes}** minutes **{seconds}** seconds"
    )
    return uptime_stamp
