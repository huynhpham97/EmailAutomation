import os
import logging
import datetime
from pathlib import Path

PATH_LOG = "output/log/"

def setup_logging():

    Path(PATH_LOG).mkdir(parents=True, exist_ok=True)

    current_date = datetime.datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(PATH_LOG, f"email_send_automation_{current_date}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger("email_send_automation")
    return logger, log_file