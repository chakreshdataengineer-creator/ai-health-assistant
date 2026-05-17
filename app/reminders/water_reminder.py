from apscheduler.schedulers.background import BackgroundScheduler

def water_reminder():

    print("💧 Reminder: Drink 500ml water now!")

scheduler = BackgroundScheduler()

scheduler.add_job(
    water_reminder,
    'interval',
    hours=2
)

scheduler.start()