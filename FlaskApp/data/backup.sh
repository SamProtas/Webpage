#!/bin/bash

thedate=`date +%F`
oldname="_HG.db"
#echo `date +%F`

newname=$thedate$oldname

cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd
cp HG.db db_backup/$newname
