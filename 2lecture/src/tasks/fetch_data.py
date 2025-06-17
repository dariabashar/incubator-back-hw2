from main import celery

@celery.task
def fetch_data():
    print("Fetching data from website...")