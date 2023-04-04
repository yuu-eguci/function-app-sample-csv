import datetime
import logging

import azure.functions as func
from sample_csv_function.example import read_csv_to_dicts


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    logging.info(read_csv_to_dicts('./sample_csv_function/jason_statham.csv'))
