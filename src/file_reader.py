import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from logger.logger_config import setup_logging

SHEET_URL = "https://docs.google.com/spreadsheets/d/1RaJL2qbv8n1n_j6rYXNxmO_crmYOzIcPJ_emVLjknfw"
CREDENTIALS_PATH = "authen/credentials.json"

OUTPUT_FILE = "output/filtered_data.xlsx"


class GoogleSheetFilter:

    def __init__(self):
        self.client = self._authenticate()
        self.logger, self.log_file = setup_logging()

    def _authenticate(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
        return gspread.authorize(creds)

    def filter_and_save(self):
        try:
            spreadsheet = self.client.open_by_url(SHEET_URL)
            all_sheets = spreadsheet.worksheets()
            
            self.logger.info(f"Found {len(all_sheets)} sheets in the Google Sheet.")

            with pd.ExcelWriter(OUTPUT_FILE) as writer:
                for sheet in all_sheets:
                    
                    self.logger.info(f"Processing sheet: '{sheet.title}'")
                    
                    df = get_as_dataframe(sheet, evaluate_formulas=True, header=None)

                    df[0] = df[0].ffill()

                    df_filtered = df[df[0].astype(str).str.contains('B', na=False)]

                    df_result = df_filtered.iloc[:, [0] + list(range(4, len(df.columns)))]

                    if not df_result.empty:
                        df_result.to_excel(writer, sheet_name=sheet.title, index=False, header=False)
                        self.logger.info(f"Saved {len(df_result)} rows from '{sheet.title}'")

            self.logger.info(f"Done! Data has been saved: '{OUTPUT_FILE}'")
            # print(f"Done! Data has been saved: '{OUTPUT_FILE}'")
            
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}", exc_info=True)
