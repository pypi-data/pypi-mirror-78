from __future__ import print_function
import sys
import logging

if sys.version_info[0] < 3:
    from urlparse import parse_qsl
    from urllib2 import urlopen, HTTPCookieProcessor
    from urllib import urlencode
else:
    from urllib.parse import parse_qsl, urlencode
    from urllib.request import urlopen, HTTPCookieProcessor, build_opener

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename="log.txt")


def token_getter_url(**kwargs):
    return "https://oauth.vk.com/authorize?" + urlencode(kwargs)


def parse_token(url_with_token):
    qsl = parse_qsl(url_with_token.split("#", 1)[1])
    token = {}

    for el in qsl:
        token[el[0]] = el[1]

    return token


def get_token_cmd(app_id, api_ver='5.64', scope=0):
    if sys.version[0] < 3:
        from cookielib import CookieJar
    else:
        from http.cookiejar import CookieJar
    redirect_uri = 'https://oauth.vk.com/blank.html'
    op = build_opener()
    op.addheaders.append(('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'))
    op.addheaders.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))
    op.addheaders.append(('Accept-Language', 'en-US;q=0.5,en;q=0.3'))

    cj = CookieJar()
    op.add_handler(HTTPCookieProcessor(cj))

    r = op.open(token_getter_url(
        client_id=app_id,
        scope=scope,
        redirect_uri=redirect_uri,
        display="wap",
        v=api_ver,
        response_type='token'
    ))
    print(r.read())


def get_token_gui(app_id, api_ver='5.64', scope=0, storage="", no_show=False):
    import subprocess
    import os
    import json
    import tempfile
    log.debug("obtaining token through gui")

    redirect_uri = 'https://oauth.vk.com/blank.html'

    exec = os.path.join(os.path.dirname(__file__), "pyvklogin_ext.py")
    python_exec = sys.executable
    if os.name == "nt" and sys.executable.endswith("python.exe"):
        python_exec = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
        if not os.path.isfile(python_exec):
            python_exec = sys.executable

    out = tempfile.NamedTemporaryFile(delete=False)
    out_fn = out.name
    out.close()

    args = [python_exec, exec,
        "--output", out_fn,
        "--storage", storage,
        "--redirect_uri", redirect_uri,
        "--app_id", str(app_id),
        "--api_version", api_ver,
        "--scope", str(scope)
    ]

    if no_show:
        args.append("--no_show")

    ret = subprocess.run(args)
    if ret.returncode != 0:
        return {"error": ret}
    else:
        with open(out_fn, "r+") as f:
            ret = json.load(f)
        os.remove(out_fn)

    return ret


if __name__ == "__main__":
    app_id = 4527090
    api_version = "5.122"
    log.info("starting")

    token = get_token_gui(app_id=app_id, api_ver=api_version, scope=5, storage="""vkstorage""")
    log.info(token)
    import urllib
    import json
    req = urllib.request.Request(
        f'https://api.vk.com/method/users.get?access_token={token["access_token"]}&v={api_version}')
    with urllib.request.urlopen(req) as res:
        res = json.load(res)
        log.info(res)
        print(res)
