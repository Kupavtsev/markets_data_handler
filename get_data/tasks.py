from celery import shared_task
from .binance_api import data_from_binance

@shared_task(bind=True)
def test_func(self):
    # response = data_from_binance(assets)
    # print(response)
    # save data to DB

    return "done"