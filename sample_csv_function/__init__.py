import datetime
import logging

import azure.functions as func

from sample_csv_function.example import CSV_PATH, read_csv_to_dicts


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now(datetime.UTC).isoformat()

    if mytimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function ran at %s", utc_timestamp)
    rows = read_csv_to_dicts(CSV_PATH)
    logging.info("Loaded %d rows from %s", len(rows), CSV_PATH)
    for row in rows:
        logging.info("%(year)s %(title)s / %(role)s", row)
