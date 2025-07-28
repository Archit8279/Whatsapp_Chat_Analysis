import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    
    # Regex to split messages on timestamp
    pattern = r"(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}(?:\u202f|\s)?[ap]m)\s[-–]\s"

    # Split messages
    messages = re.split(pattern, data)[1:]

    # Group into triplets: [datetime1, message1, datetime2, message2, ...]
    # So we take even indexes as datetime, odd indexes as message
    dates = messages[0::2]
    msgs = messages[1::2]

    user_messages = []
    formatted_dates = []

    for date_str, message in zip(dates, msgs):
        try:
            dt = datetime.strptime(date_str.strip(), "%d/%m/%y, %I:%M %p")
        except ValueError:
            continue  # skip malformed timestamps

        # Extract user and message
        if ':' in message:
            user, msg = message.split(":", 1)
        else:
            user = "group_notification"
            msg = message

        user_messages.append({'date': dt, 'users': user.strip(), 'messages': msg.strip()})

    # Create DataFrame
    df = pd.DataFrame(user_messages)

    # Preview
    df.head()

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df['only_date'] = df['date'].dt.date
    df['year']=df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['dayname'] = df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute


    period = []
    for hour in df[['dayname', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))

    df['period'] = period

    return df
