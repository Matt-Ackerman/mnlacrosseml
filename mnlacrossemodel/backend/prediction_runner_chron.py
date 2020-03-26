from apscheduler.schedulers.background import BackgroundScheduler
from mnlacrossemodel.backend.prediction_runner import PredictionRunner


def start():
    """
    1. Creates the chron job which moves current live predictions to results and then brings in the new predictions.
    """

    predictor = PredictionRunner()
    scheduler = BackgroundScheduler()

    scheduler.add_job(predictor.move_live_predictions_to_results, 'interval', minutes=1)
    scheduler.add_job(predictor.create_live_predictions, 'interval', minutes=1)

    scheduler.start()
