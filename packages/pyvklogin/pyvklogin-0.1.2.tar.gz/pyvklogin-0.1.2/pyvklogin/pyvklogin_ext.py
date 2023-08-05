from __future__ import print_function
import logging
import sys
import json

if sys.version_info[0] < 3:
    from urlparse import parse_qsl
    from urllib2 import urlopen, HTTPCookieProcessor
    from urllib import urlencode
else:
    from urllib.parse import parse_qsl, urlencode
    from urllib.request import urlopen, HTTPCookieProcessor, build_opener

log = logging.getLogger(__file__)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage

import argparse

parser = argparse.ArgumentParser(description='inner authorization application')
parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help="Set the logging level", default="WARNING")
parser.add_argument(
    '--logfile',
    help="log file instead of stderr",
    type=str,
    default=""
)
parser.add_argument(
    '--storage',
    help="app storage",
    type=str,
    default=""
)
parser.add_argument(
    '--redirect_uri',
    type=str,
    default="https://oauth.vk.com/blank.html"
)
parser.add_argument(
    '--app_id',
    type=int,
    default=0
)
parser.add_argument(
    '--scope',
    type=int,
    default=0
)
parser.add_argument(
    '--state',
    type=str,
    default=""
)
parser.add_argument(
    '--api_version',
    type=str,
    default=""
)
parser.add_argument(
    '--no_show',
    action="store_const", dest="no_show", const=True,
    default=False
)
parser.add_argument(
    '--output',
    type=str,
    default="-"
)

args, rest_args = parser.parse_known_args()

logging_kwargs = {}
if args.logfile != "":
    logging_kwargs["filename"] = args.logfile
logging.basicConfig(level=getattr(logging, args.logLevel), **logging_kwargs)
log.debug("starting subprocess")

log.debug("args: " + repr(args))

app = QApplication([])
browser = QWebEngineView()

if args.storage != "":
    log.debug("using storage " + args.storage)
    profile = QWebEngineProfile(args.storage, browser)
    webpage = QWebEnginePage(profile, browser)
    browser.setPage(webpage)

redirect_uri = args.redirect_uri

def parse_token(url_with_token):
    qsl = parse_qsl(url_with_token.split("#", 1)[1])
    token = {}

    for el in qsl:
        token[el[0]] = el[1]

    return token

def token_getter_url(**kwargs):
    return "https://oauth.vk.com/authorize?" + urlencode(kwargs)

def url_listener(url):
    global finished_url
    url_s = url.toString()
    log.info("new location: " + url_s)
    if url_s.startswith(redirect_uri):

        token = parse_token(url_s)
        if args.state == "" or ("state" in token and token["state"] == args.state):
            if args.output != "-":
                with open(args.output, "w+") as f:
                    json.dump(token, f)
            else:
                json.dumps(token)
            browser.close()

browser.urlChanged.connect(url_listener)

browser.load(QUrl(token_getter_url(
    client_id=args.app_id,
    scope=args.scope,
    redirect_uri=redirect_uri,
    v=args.api_version,
    response_type='token'
)))
if not args.no_show:
    browser.show()

ret = app.exec()
exit(ret)
