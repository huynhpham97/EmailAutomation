
from logger.logger_config import setup_logging
from src.file_reader import GoogleSheetFilter



logger, log_file = setup_logging()
logger.info("======================= Start Process Generator File =======================")

sheet_filter = GoogleSheetFilter()
sheet_filter.filter_and_save()



    