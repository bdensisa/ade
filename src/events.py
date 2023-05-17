# Import
from requests import get
from ics import Calendar

# Fetch events for an URL
def fetch_events(url):
    # Fetch calendar
    try:
        calendar = Calendar(get(url).text)
        return calendar.events
    except:
        return []
