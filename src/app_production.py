import logging
from httpserver import HTTPServer

if __name__ == "__main__":
    HTTPServer(botLoggingLevel=logging.DEBUG,
               httpServerLoggingLevel=logging.DEBUG)
