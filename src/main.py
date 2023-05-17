# Import
from time import sleep
from datetime import datetime
from ade import load_user
from database import get_users, update_courses
from events import fetch_events

min_interval = 60 * 60 # In seconds
last_refresh = None

# Main loop
while True:
    # We check if we need to refresh
    while last_refresh is not None and (datetime.now() - last_refresh).total_seconds() < min_interval:
        sleep(10)

    # We refresh everything
    last_refresh = datetime.now()
    users = get_users()
    for user in users:
        id = user[0]
        email = user[1]
        first_name = user[3]
        last_name = user[4]
        url = load_user(last_name)
        events = fetch_events(url)
        update_courses(events, id)
