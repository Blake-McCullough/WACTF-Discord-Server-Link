import requests
import os

def exchange_code(code):
  data = {
    'client_id': os.getenv("CLIENT_ID"),
    'client_secret': os.getenv("CLIENT_SECRET"),
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': os.getenv("REDIRECT_URI")
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post(url='https://discord.com/api/v10/oauth2/token', data=data, headers=headers)
  r.raise_for_status()
  data = r.json()
  return data['access_token']

def get_user_id(token):

    headers = {
        'Authorization': 'Bearer ' + token
    }
    r = requests.get(url='https://discord.com/api/v10/users/@me',  headers=headers)
    r.raise_for_status()
    data = r.json()
    return data['id']

import requests
def join_discord(token,user_id):
    
    print("Joining")
    url = "https://discord.com/api/v10/guilds/"+os.getenv("GUILD_ID")+"/members/"+str(user_id)
    print(url)
    payload = '{\"access_token\": \"'+str(token)+'\"}'
    headers = {
        'authorization': "Bot " + os.getenv("BOT_TOKEN"),
        'content-type': "application/json",


        }

    response = requests.request("PUT", url, data=payload, headers=headers)
    print(response.status_code)
    if response.status_code == 201:
        return True
    elif response.status_code ==204:
        return False
    else:
        return None

def get_username_by_id(user_id):
    url = "https://discord.com/api/v10/users/"+str(user_id)


    headers = {
        'authorization': "Bot " + os.getenv("BOT_TOKEN")
       
        }

    response = requests.request("GET", url,  headers=headers)
    if response.status_code == 201 or response.status_code ==200 or response.status_code ==204:
        data = response.json()
        user_name = data['username']
        tag = data['discriminator']
        user_name_tag = user_name+"#"+tag
        return user_name_tag
    else:
        return None
import json
import requests

def get_users_count_for_role(role_ID):
    url = "https://discord.com/api/v10/guilds/598006801715298305/members?limit=1000"

    payload={}
    headers = {
    'authorization': 'Bot MTAxMjU3MDQzMDI5MDI3MjI2Ng.GlaT7p.t-LbWH1AwL32nZou8K3NvV1c6hf0DVanqeGfyk',
    'Cookie': '__dcfduid=bd836b702a8811ed930c169e368c4e8a; __sdcfduid=bd836b702a8811ed930c169e368c4e8aad904174c95a1fc6091f6a6a27ba3c46567d37292038187b3d504b4184d85da3'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    count = 0
    for user in data:
        #print(user)
        if role_ID in user["roles"]:
            count = count+1
    return count


def edit_voice_channel_name(channel_id,name):

    url = "https://discord.com/api/v10/channels/"+channel_id

    payload = json.dumps({
    "name": name
    })
    headers = {
    'authorization': 'Bot MTAxMjU3MDQzMDI5MDI3MjI2Ng.GlaT7p.t-LbWH1AwL32nZou8K3NvV1c6hf0DVanqeGfyk',
    'Content-Type': 'application/json',
    
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    print(response.status_code)




if __name__ == "__main__":
    get_username_by_id()