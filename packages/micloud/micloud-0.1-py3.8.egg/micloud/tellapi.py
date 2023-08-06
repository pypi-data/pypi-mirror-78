import argparse
import falcon
import time
import socket
from wsgiref import simple_server

import logging
from logging.handlers import TimedRotatingFileHandler

import config
from light import Light
from utils import log_msg
from config import Flag
from tellstick.tdtool import TdTool
from api import AuthMiddleware, json_serializer


app = falcon.App(middleware=[ AuthMiddleware(),])
app.set_error_serializer(json_serializer)

def start_server():
    log_msg("Starting http server.", color="green", level=logging.INFO)

    # Get ip to bind server on
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    log_msg("Binding IP: " + ip, level=logging.DEBUG, offset=True)
    log_msg("Port: 8000", level=logging.DEBUG, offset=True)

    httpd = simple_server.make_server(ip, 8000, app)
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tellstick API')
    parser.add_argument('-log', default='logs/tellapi.log', help='Log file.')
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help='debug mode.')
    parser.add_argument('--sim', dest='sim', default=False, action='store_true', help='Run in sim mode.')

    args = parser.parse_args() 
    #args, unknown = parser.parse_known_args()
    config.DEBUG = args.debug
    config.SIMULATE = args.sim

    # Configure logger
    config.LOGGER = logging.getLogger("tellapi")
    if config.DEBUG:
        config.LOGGER.setLevel(logging.DEBUG)
    else:
        config.LOGGER.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(args.log, when="d", interval=1, backupCount=7)
    f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d %b %H:%M:%S')
    handler.setFormatter(f_format)
    config.LOGGER.addHandler(handler)
    config.LOGGER.propagate = False

    log_msg("[!] Starting tellapi.", color="gray")
    light = Light()
    app.add_route('/light', light)

    start_server()
    log_msg("[!] Tellapi Stopped.", level=logging.INFO, color='red')