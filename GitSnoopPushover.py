#!/bin/env python3

# Written by Rob Probin 8 July 2016,  Licensed under the "MIT license", as follows
#
# Copyright (c) 2016 Rob Probin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this 
# software and associated documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to the following 
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies 
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

CHECK_ALL_BRANCHES = True

if CHECK_ALL_BRANCHES:
    #  Other items considered: --source --remotes
    cmd = 'git log --all --format="%an %d %s" --graph --since "{time}"'    # all branches
else:
    cmd = 'git log --format="%an %s" --since "{time}"'

MAX_PUSH_LENGTH = 1024

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
    
    
    
def get_log(repo, time, not_starts_with):
    out = subprocess.check_output(cmd.format(time=time), cwd=repo, shell=True)
    
    # decode, and ignore errors
    out = out.decode("utf-8", errors="ignore")

    out = out.strip()

    if not_starts_with is not None:
        revlist = out.split('\n')
        outlist = []
        #print(revlist)
        for l in revlist:
            if not l.startswith(not_starts_with):
                outlist.append(l+'\n')
        
        out = "".join(outlist)
        out = out.strip()

    if len(out) > MAX_PUSH_LENGTH:
        out = out[:MAX_PUSH_LENGTH-4] + " ..."
    
    if len(out) == 0:
        out = None

    #print(out)
    return out


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print('Arguments: git-repo-URL "time since" [pushover-app-key pushover-user-key] ["name starts with filter"]')
        print('Example:   . "600 seconds ago" abfe4545fpowe4534 22b32323rr232')

        sys.exit(1)

    repo = sys.argv[1]
    time = sys.argv[2]

    appkey = None
    userkey = None
    if len(sys.argv) > 4:
        appkey = sys.argv[3]
        userkey = sys.argv[4]

    not_starts_with = None
    if len(sys.argv) == 6:
        not_starts_with = sys.argv[5]
    elif len(sys.argv) == 4:
        not_starts_with = sys.argv[3]
    
    log = get_log(repo, time, not_starts_with)
    if log != None:
        if appkey is not None:
            send_message(log, appkey, userkey)
        else:
            print(log)
    else:
        print("Nothing to do")

main()


