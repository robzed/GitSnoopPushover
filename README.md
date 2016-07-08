Git Snoop Pushover
==================

When run pushes via PushOver.net if anything has been committed.

Run from the command line like this...
--------------------------------------

python3 GitSnoopPushover.py <git-repo-URL> "<time since>" <pushover-app-key> <pushover-user-key>

python3 GitSnoopPushover.py . "600 seconds ago" 234afij3rksmfsdiofj3 3kjesfi4rt39ufeoijsf


Run from a CRON script like this...
-----------------------------------

For every 10 minutes, use 'crontab -e' and insert:

*/10 * * * * python3 GitSnoopPushover.py some/dir "10 minutes ago" 234afij3rksmfsdiofj3 3kjesfi4rt39ufeoijsf

You might need to change directory, depending on things (always try python3 GitSnoopPushover.py with arguments on the command line first to see what is happening) - this assumes that the GitSnooperPushover.py is in your home directory:

*/10 * * * * cd some/dir && python3 ~/GitSnoopPushover.py . "10 minutes ago" 234afij3rksmfsdiofj3 3kjesfi4rt39ufeoijsf


**Note:** There is a good chance that cron tasks don't run exactly 10 minutes apart - in that case, you have some non-zero chance of missing a specific commit. If that is important then you have three choices:
1. Don't use this tool.
2. Specify a slightly longer time (e.g. 610 seconds ago) and realise that you might get some committ messages twice.
3. Modify the code to store the last revision fetched somewhere, and use that instead (or as well as) the time window.


For more Cron Help, this is a pretty good page https://help.ubuntu.com/community/CronHowto


License
-------

Licensed under the MIT license - see file headers or 'LICENSE'.


