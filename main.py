from dotenv import load_dotenv

from teams_discord import start_up
import web_server


#For event that occurs every x minutes.
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler



#scheduler = BackgroundScheduler()
#scheduler.add_job(func=run_edits, trigger="interval", seconds=60)
#scheduler.start()




if __name__ == "__main__":
    
    load_dotenv()
    start_up()
    web_server.start()

    
    