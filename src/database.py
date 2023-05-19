# Import
from os import getenv
from mysql.connector import connect
from datetime import datetime

# Connect to database
mydb = connect(
    host=getenv('DB_HOST'),
    user=getenv('DB_USER'),
    password=getenv('DB_PASSWORD'),
    database=getenv('DB_NAME')
)

def transform_date(date):
    return date.format('YYYY-MM-DD[T]HH:mm:ss[Z]')

def transform_description(description):
    return ", ".join(filter(
        lambda line: line and not line.startswith('(Exporté le'),
        description.split('\n')
    ))

def get_users():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, first_name, last_name FROM Users")
    return mycursor.fetchall()

def update_courses(events, user_id):
    # First delete courses that are not longer in the calendar
    mycursor = mydb.cursor()
    mycursor.execute(
        "DELETE FROM UserCourses WHERE user_id = %s AND ade_uid NOT IN (%s)",
        (user_id, ','.join([event.uid for event in events]))
    )
    mydb.commit()

    # Then update or insert courses (we're using upsert to do it in one query)
    mycursor = mydb.cursor()
    sql = "INSERT INTO UserCourses (ade_uid, user_id, title, start, end, location, description) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = VALUES(title), start = VALUES(start), end = VALUES(end), location = VALUES(location), description = VALUES(description)"
    values = [
        (event.uid, user_id, event.name, transform_date(event.begin), transform_date(event.end), event.location, transform_description(event.description))
        for event in events
    ]
    mycursor.executemany(sql, values)
    mydb.commit()
