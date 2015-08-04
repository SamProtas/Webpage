git push origin master && ssh -p 2225 jmc856@104.236.16.76 "cd /var/www/FlaskApp && sudo git pull origin master && sudo apache2ctl graceful"
