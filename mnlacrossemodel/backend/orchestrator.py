from apscheduler.schedulers.background import BackgroundScheduler
from mnlacrossemodel.backend.prediction_runner import PredictionRunner


def start():
    predictor = PredictionRunner()
    scheduler = BackgroundScheduler()

    scheduler.add_job(predictor.create_upcoming_game_predictions, 'interval', minutes=1)
    scheduler.add_job(predictor.create_past_game_predictions, 'interval', minutes=1)
    scheduler.start()
