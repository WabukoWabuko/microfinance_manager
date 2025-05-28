import sys
import logging
from src.ui_manager import UIManager
from src.database import Database

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='a',
                       format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug("Starting main.py")
    try:
        logging.debug("Initializing Database")
        database = Database()
        logging.debug("Initializing UIManager")
        ui_manager = UIManager(database)
        logging.debug("UIManager initialized, starting app")
        sys.exit(ui_manager.app.exec_())
    except Exception as e:
        logging.error(f"Error in main.py: {str(e)}")
        print(f"Error in main.py: {e}")
