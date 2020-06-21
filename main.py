from twython import Twython
import json
import pandas as pd
import csv


with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])


query = {'q': 'mask',
         'result_type': 'popular',
         'count':5,
         'lang': 'en',
         }

csv_file = "Names2.csv"
csv_columns = ['screen_name', 'userid', 'name', 'description', 'location', 'hashtags', 'mentions', 'date', 'favorite_count', 'id', 'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', 'text']

dict_ = {'screen_name': [], 'userid': [], 'name': [], 'description': [], 'location': [], 'hashtags': [], 'mentions': [], 'date': [], 'favorite_count': [], 'id': [], 'in_reply_to_status_id': [], 'in_reply_to_user_id': [], 'in_reply_to_screen_name': [], 'text': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['screen_name'].append(status['user']['screen_name'])
    dict_['userid'].append(status['user']['id'])
    dict_['name'].append(status['user']['name'])

    dict_['description'].append(status['user']['description'])
    dict_['location'].append(status['user']['location'])

    dict_['hashtags'].append(status['entities']['hashtags'])
    dict_['mentions'].append(status['entities']['user_mentions'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])
    dict_['id'].append(status['id'])
    dict_['in_reply_to_status_id'].append(status['in_reply_to_status_id'])
    dict_['in_reply_to_user_id'].append(status['in_reply_to_user_id'])
    dict_['in_reply_to_screen_name'].append(status['in_reply_to_screen_name'])


zd = zip(*dict_.values())
with open(csv_file, 'w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(dict_.keys())
    writer.writerows(zd)



df = pd.DataFrame(dict_)
df.sort_values(by='favorite_count', inplace=True, ascending=False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)
print(df.head(5))

