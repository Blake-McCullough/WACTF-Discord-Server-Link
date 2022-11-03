import json
import sqlite3


#For when the server first starts up.
def start_up():
    '''Sets up the database file with details needed.'''
    #Opens the database file.
    con = sqlite3.connect("database.db")
    #Opens cursor for commands.
    cur = con.cursor()
    #Creates the database (If it does not exist).
    cur.execute('''CREATE TABLE IF NOT EXISTS discordTeamsLink(
                ID INTEGER PRIMARY KEY,
                discordID VARCHAR(255) NOT NULL,
                teamID VARCHAR(255) NOT NULL,
                setDate DATETIME NOT NULL
                );''')
    #Executes command.
    con.commit()
    #Closes connection.
    con.close()

def get_discord_details(TEAM_ID,DISCORD_ID):
    '''Fetches all details stored for given team_id and discord_id.'''
    #Opens connection to database.
    con = sqlite3.connect("database.db")
    #Opens cursor for commands.
    cur = con.cursor()
    results = []
    for row in cur.execute("SELECT teamID,discordID,setDate FROM discordTeamsLink WHERE teamID=:teamID AND discordID=:discordID;",{"teamID": TEAM_ID,"discordID":DISCORD_ID}):
        #Adds to results. 
        results.append({"Team_ID":row[0],"Discord_ID":row[1],"Set_Date":str(row[2])})
    return results

#To be sorted out into a SQL database.
def fetch_team_discords(TEAM_ID):
    '''Gets a list of discord ID's from a team ID.'''
    #Opens connection to database.
    con = sqlite3.connect("database.db")
    #Opens cursor for commands.
    cur = con.cursor()
    results = []
    for row in cur.execute("SELECT discordID FROM discordTeamsLink WHERE teamID=:teamID;",{"teamID": TEAM_ID}):
        #Adds to results. 
        results.append(row[0])
    return results


def save_discord_id(TEAM_ID,DISCORD_ID):
    '''Saves a discord ID to a teams ID, returns false if exists, true if doesn't.'''
    #Ensure doesn't exist already.
    if len(get_discord_details(TEAM_ID,DISCORD_ID)) == 0:
        #Opens connection to database.
        con = sqlite3.connect("database.db")
        #Opens cursor for commands.
        cur = con.cursor()
        #Adds the user and all details to database.
        cur.execute("insert into discordTeamsLink(discordID,teamID,setDate) values (?,?,datetime('now'))", (DISCORD_ID,TEAM_ID))
        #Executes command.
        con.commit()
        #Closes connection.
        con.close()
        return True
    else:
        return False

if __name__ == "__main__":
    start_up()
    print(fetch_team_discords("23"))
    print(save_discord_id("23","2"))
