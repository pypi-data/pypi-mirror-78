import logging
import sys
import time

from take_a_break.configuration import CONFIG
from take_a_break.gui.tbmain import TBMain

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

if __name__ == '__main__':
    try:
        logging.info('Application started!')
        while True:
            TBMain().show()
            time.sleep(CONFIG.remind_me_after_this_period())
    except KeyboardInterrupt:
        logging.info("Bye, bye...")
        sys.exit()
