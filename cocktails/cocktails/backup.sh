#!/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/skillatlas/actions-runner/backend-cocktails/backend-cocktails/cocktails
now=$(date +"%d-%m-%y%H:%M:%S")
filename=backups/cocktails$now.json
docker exec skill01 python manage.py dumpdata -o $filename -a
