#!/usr/bin/env python3

# Standard library imports
import logging
import os.path
import sys

# Local application/library specific imports
from libraries.libmango import *
from libraries.Questions import *
from libraries.libguava import *
from libraries.libadb import *
from libraries.logging_config import setup_logging


logging.getLogger().handlers = []  
setup_logging() 
logger = logging.getLogger(__name__)

def print_logo():
    print(Style.BRIGHT + BLUE + """
  Welcome to
        
    888b     d888                                    
    8888b   d8888                                    
    88888b.d88888                                    
    888Y88888P888  8888b.  88888b.   .d88b.   .d88b. 
    888 Y888P 888     "88b 888 "88b d88P"88b d88""88b
    888  Y8P  888 .d888888 888  888 888  888 888  888
    888   "   888 888  888 888  888 Y88b 888 Y88..88P
    888       888 "Y888888 888  888  "Y88888  "Y88P" 
                                        888         
                                    Y8b d88P         
                                    "Y88P"           """ + Style.RESET_ALL + RESET)

def start_session(db_session, existing=False):
    application_database = apk_db(db_session)
    guava = Guava(application_database)
    p = parser()
    p.database = application_database
    p.guava = guava
    if existing:
        p.continue_session(guava)
    p.device = p.get_device()
    p.cmdloop()


if __name__ == "__main__":
    print_logo()
    if len(sys.argv) > 1:
        session = sys.argv[1]

        if os.path.exists(session):
            start_session(session, True)
        else:
            logger.error(f"Can't find: {session} ")
            sys.exit()
    else:
        menu = {}
        menu['1'] = "Start a new session"
        menu['2'] = "Continue an existing session"
        menu['3'] = "Exit"
        while True:
            print("-" * 50 + "\n[?] What do you want to do ?\n" + "-" * 50)
            options = menu.keys()

            for entry in options:
                print(entry, menu[entry])
            selection = input("\n[?] Enter your selection: ")

            if selection == '1':
                session = input("\n[?] Enter a session name: ")
                start_session(session)
                break
            elif selection == '2':
                session = input("\n[?] Enter full path to the session file: ")
                if os.path.exists(session):
                    start_session(session, True)
                else:
                    logger.error(f"Can't find: {session} ")
                    sys.exit()
                break
            elif selection == '3':
                sys.exit()
            else:
                logger.warning("Unknown Option Selected!")
