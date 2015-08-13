#!/bin/bash

thedate=`date +%F`
oldname="_fantasy_football.db"
#echo `date +%F`

newname=$thedate$oldname

cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd
cp fantasy_football.db db_backup/$newname
