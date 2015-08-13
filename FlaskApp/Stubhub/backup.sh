#!/bin/bash

thedate=`date +%F`
oldname="_stubhub.db"
#echo `date +%F`

newname=$thedate$oldname

cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd
cp data/stubhub.db data/db_backup/$newname
