import threading
import time
import schedule
from discover import db
from wikidataDiscovery import logs
from .wd_utils import update_cache_log


def run_continuously(interval=120):
    """Function is called during startup of DiscoverApp by overriding the AppConfig.ready method.  Every 120 seconds,
    it checks for scheduled jobs defined with the external 'schedule' library and executes them on a background thread.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


# Job: cache all app wikidata in backend.
def cache_wikidata():
    msgs = db.cache_all()
    update_cache_log(msgs)


# Job: rotate logs, making issue.log issue.log.1, etc.
def rotate_logs():
    logs.rotate_logs()


def background_job():
    print('Hello from the background thread')


# Use schedule module to define jobs for specific times
schedule.every().day.at('23:55').do(cache_wikidata)
schedule.every().day.at('00:01').do(rotate_logs)
# schedule.every(10).seconds.do(background_job)


# Stop the background thread
# stop_run_continuously.set()
