#!/bin/env python3

GIT_TIME_PERIOD_IN_SECONDS = 600

cmd = 'git log --format="%an %s" --since "{time}" {repo}'

MAX_PUSH_LENGTH = 250

import subprocess
import sys
import http.client, urllib

def send_message(message, appkey, userkey):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": appkey,
        "user": userkey,
        "message": message,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    
    
    
def get_log(repo, time):
    out = subprocess.check_output(cmd.format(repo=repo, time=time), shell=True)
    
    # decode, and ignore errors
    out = out.decode("utf-8", errors="ignore")

    out = out.strip()
    
    if len(out) > MAX_PUSH_LENGTH:
        out = out[:MAX_PUSH_LENGTH-4] + " ..."
    
    if len(out) == 0:
        out = None

    return out


def main():
    if len(sys.argv) != 5:
        print('Arguments: git-repo-URL "time since" pushover-app-key pushover-user-key')
        print('Example:   . "600 seconds ago" abfe4545fpowe4534 22b32323rr232')
        sys.exit(1)

    repo = sys.argv[1]
    time = sys.argv[2]
    appkey = sys.argv[3]
    userkey = sys.argv[4]
    log = get_log(repo, time)
    if log != None:
        send_message(log, appkey, userkey)
    else:
        print("Nothing to do")

main()


