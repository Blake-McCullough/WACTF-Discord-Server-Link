from operator import itemgetter
import requests
import os
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from discord_oauth import edit_voice_channel_name, get_users_count_for_role

from datetime import datetime,timezone
from collections import defaultdict
import time

        
def send_edit_embed(message_url,message,title):
    '''Send the request to change the embed for the channel.'''
     #Gets current time.
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


    #Sends of editing message.
    payload = {
        'embeds':
        [
            {
                'title':title,
                'type':'rich',
                'description':message,
                'color':7419530,
                'timestamp':now,
                'author':
                {
                    'name':'PECAN CTF 2022',
                    'url':'https://blakemccullough.com/'
                },
                'footer':
                {
                    'text':'By Blake McCullough'
                }   
            }
        ]
    }
    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }

    response = requests.request("PATCH", message_url, json=payload, headers=headers)

    if response.status_code == 204 or response.status_code==200:
        pass
    elif response.status_code == 429:
        print(int(response.headers["Retry-After"]))
        print(response.headers['x-ratelimit-scope'])
        print('Embed error: ' +str(response.status_code))
        print(response.headers)
    else:
        print('Embed error: ' +str(response.status_code))
        print(response.headers)
      
def extract_categories_message(data):
    '''Takes a list of challenges, returns a message with the categories and then the amount off solves'''

    #Sets as blank due to none being specified.
    counts = defaultdict(int)
    #loops through data setting key as the category name, and value as the amount of solves.
    for d in data:
        counts[d.get("category")] += d.get("solves")
    #Sorts the categories from most to least and converts to list.
    counts_sorted = sorted(counts.items(), key=lambda x: x[1],reverse = True)
    #Starting message.
    message = '__**Name: Solves **__\n\n'
    #Extracts the key and value from each element, then will add it to the message.
    for key, value in counts_sorted:
        message = message + f'**{key}:** {value}\n'
    return message
    
def send_updates_message(message):
    response = DiscordWebhook(url=os.getenv('GAME_WEBHOOK_URL'), content=message).execute()

def send_linking_message(message):
    response = DiscordWebhook(url=os.getenv('LINKING_WEBHOOK_URL'), content=message).execute()   

def give_user_role(Member_ID,Role_ID):
    '''Uses the discord API to give a user a role, then will return true on success, false on error.'''
    url = "https://discord.com/api/guilds/"+os.getenv("GUILD_ID")+ "/members/"+Member_ID+'/roles/'+Role_ID
    print(url)

    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }
    response = requests.request("PUT", url,  headers=headers)
    if response.status_code == 204:
        return True
    else:
        print(response.status_code)
        return False
  
def give_team_division_role(user_id,division):
    try:
        #RoleID is determined based on what the skill id is.
        beginner_division = os.getenv('BEGINNER_DIVISION')
        intermediate_division = os.getenv('INTERMEDIATE_DIVISION')
        advance_division = os.getenv('ADVANCED_DIVISION')
        print(beginner_division)
        print(intermediate_division)
        print(advance_division)
        if division == beginner_division:
            role_id = os.getenv('BEGINNER_ROLE_ID')
        elif division == intermediate_division:
            role_id = os.getenv('INTERMEDIATE_ROLE_ID')
        elif division ==  advance_division:
            role_id = os.getenv('ADVANCED_ROLE_ID')
        else:
            send_linking_message(f'Failed to give the user: {user_id} a role, as division was: {division}')
            return
        give_user_role(Member_ID= user_id,Role_ID = role_id)
    except Exception as e:
        print(e)

if __name__ == "__main__":
   
    load_dotenv()
    #create_graph_message()
