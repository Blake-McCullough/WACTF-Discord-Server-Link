
# importing modules
import datetime,flask,os
from flask import Flask,  redirect, request,Response, render_template, abort, redirect, request,  Response, render_template, make_response,url_for
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
from discord_oauth import exchange_code, get_user_id, get_username_by_id, join_discord

from discord_server_link import give_user_role, send_linking_message,  send_updates_message
from role_score_link import get_role_given
from teams_discord import fetch_team_discords, save_discord_id




load_dotenv()


# declaring app name
app = Flask(__name__)
#For adding the count of said item to the manifest ID.
@app.route('/challengecomplete',methods = ['POST', 'GET'])
def pecanchallengeevent():
    if request.headers.get("X-API-Key",None) != os.getenv("SECRET_KEY"):
        abort(403)

    if request.method == 'POST':
        print('POST')
        try:
            teamid = request.args.get('teamid')
            teamname = request.args.get('teamname')
        
            challengename =request.args.get('challenge')
            #Gets current teams score.
            current_score = int(request.args.get('points'))
        except:
            abort(412)
        
        #Gets role ID, and role name
        role = get_role_given(Team_ID=teamid,Current_Score = current_score)
        
   
        #Checks if the user can recieve a role, if they can then will run this.
        if role == None:
            message = f'''**The team:** `{teamname}` | **Just completed:** `{challengename}` | **Current score:** `{current_score}`'''
        else:

            role_id = role['Role_ID']
            role_name = role['Role_Name']
            #Gets discord IDS
            discord_ids= fetch_team_discords(TEAM_ID=teamid)
            #Gives user roles.
            for user_id in discord_ids:
 
                give_user_role(Member_ID= user_id,Role_ID = role_id)


            message = f'''**The team:** `{teamname}` | **Just completed:** `{challengename}` | **Current Highest role:** `{role_name}` | **Current score:** `{current_score}`'''

        #Sends updates message
        send_updates_message(message = message)
        

        return 'Oh you made a <b>post</b> request that is pretty cool ngl!\n\n\n\nLol'
    if request.method == 'GET':
        return 'Oh you made a <b>get</b> request that is pretty not cool ngl!\n\n\n\nLol'

#For adding the count of said item to the manifest ID.
@app.route('/getdiscord')
def get_discord():
    if request.headers.get("X-API-Key",None) != os.getenv("SECRET_KEY"):
        abort(403)
    team_id =request.args.get('teamid',None)
    
    if team_id == None:
        abort(412)
    else:
        data = fetch_team_discords(team_id)
        usernames = []
        for id in data:
            username = get_username_by_id(id)
            if username == None:
                pass
            else:
                usernames.append(username)
        response = flask.jsonify({"Results":usernames })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
 



#For adding a discord user to the database (verifies via discord.)
@app.route('/adddiscord')
def add_discord():
    team_id =request.args.get('teamid',None)
    code =request.args.get('code',None)
    state =request.args.get('state',None)
    if request.headers.get("X-API-Key",None) != os.getenv("SECRET_KEY"):
        abort(403)
    if team_id == None and (code == None or state == None):
        abort(412)
    if code != None and state != None:
        try:
            #Gets token.
            token = exchange_code(code)
            print(token)
            #Gets user ID.
            user_id = get_user_id(token)
            #Saves to database.
            save_status = save_discord_id(TEAM_ID = state,DISCORD_ID = user_id)
            print(save_status)
            #Joins the discord server.
            join_discord(token,user_id)
            print("Joined")
            #For logging event.
            username = get_username_by_id(user_id)
            print(username)
            log_message = f"The user {username} just linked the team {team_id}!\n||USER ID: {user_id} and TEAM ID: {state}||"
            send_linking_message(message = log_message)
            print("Linked")
            #Redirecting back.
            return redirect(os.getenv('BASE_PECAN_URL'))    
        except:
             return redirect("https://discord.com/oauth2/authorize?client_id="+os.getenv('CLIENT_ID')+"&redirect_uri="+os.getenv('REDIRECT_URI')+"&response_type=code&scope=identify%20guilds.join&state="+state, code=302)
    else:
        return redirect("https://discord.com/oauth2/authorize?client_id="+os.getenv('CLIENT_ID')+"&redirect_uri="+os.getenv('REDIRECT_URI')+"&response_type=code&scope=identify%20guilds.join&state="+team_id, code=302)
    
def start():
    print('Web server now online.')
    app.run(host='0.0.0.0', port=80)


if __name__ == "__main__":
    start()