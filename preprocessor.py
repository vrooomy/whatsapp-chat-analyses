import re
import pandas as pd


# file_path='C:\Users\vjbro\OneDrive\Desktop\STUDY\projects\analytics\WhatsApp Chat with Oncampus placement 2025\WhatsApp Chat with Oncampus placement 2025 .txt'
# with open(file_path, 'r', encoding='utf-8') as file:
#     data = file.readlines()

# print(preprocess(data))



def preprocess(data):
    pattern = r'^(\d{2}/\d{2}/\d{2,4}, \d{1,2}:\d{2}\s?[ap]m) - (.+)$'


    dates, messages_only = [], []

    for msg in data:
        match = re.match(pattern, msg.strip())
        if match:
            dates.append(match.group(1))          # Extracted date
            messages_only.append(match.group(2)) # Extracted message

    df = pd.DataFrame({'user_message': messages_only, 'message_date': dates})

    # Convert 'message_date' to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')

    # Rename 'message_date' to 'date' (optional)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    message_pattern = '([^:]+): (.+)'

    users = []
    message = []

    for m in df['user_message']:
        entry = re.split(message_pattern, m)
        if entry[1:]:
            users.append(entry[1])
            message.append(entry[2])
        else:
            users.append('group_notif')
            message.append(m)

    df['user']= users
    df['message'] = message


    df['only_date']= df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num']= df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour']= df['date'].dt.hour
    df['minute']= df['date'].dt.minute

    period= []

    for hour in df[['day_name','hour']]['hour']:
        if hour ==23:
            period.append(str(hour)+ "-" + str('00'))
        elif hour ==0:
            period.append(str('00')+ "-" + str(hour+1))
        else:
            period.append(str(hour)+ "-" + str(hour+1))

    df['period']=period


    return df



