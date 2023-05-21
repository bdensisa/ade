# Import
from time import sleep
from datetime import datetime
from ade import init_browser, load_user, clear_browser
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
    try:
        users = get_users()
        browser = init_browser()
        for user in users:
            id = user[0]
            first_name = user[1]
            last_name = user[2]
            url = load_user(browser, last_name, first_name)
            if url is not None:
                events = fetch_events(url)
                update_courses(events, id)
        clear_browser(browser)
    except Exception as e:
        print(e)
