import smtplib 
 

def Send_Text(number, message, carrier):
	server = smtplib.SMTP( "smtp.gmail.com", 587)
	server.starttls()
	server.login("j.calvert55@gmail.com", "trIbe19t")
	user = "Jeff"
	number = str(6103063929)
	carrier = 'ATT'
	
	if carrier == 'Verizon':
		server.sendmail(user, number+ "@vzwpix.com", message)
	
	elif carrier == 'Sprint':
		server.sendmail(user, number + "@messaging.sprintpcs.net", message)	
	elif carrier == 'ATT':
		server.sendmail(user, number + "@txt.att.net", message)	

	server.quit()


#  AT&T (formerly Cingular)        [10-digit phone number]@txt.att.net
#                                 [10-digit phone number]@mms.att.net (MMS)
#                                 [10-digit phone number]@cingularme.com
#                 Example: 1234567890@txt.att.net
# Boost Mobile	                [10-digit phone number]@myboostmobile.com
#                 Example: 1234567890@myboostmobile.com
# Nextel (now Sprint Nextel)	[10-digit telephone number]@messaging.nextel.com
#                 Example: 1234567890@messaging.nextel.com
# Sprint PCS (now Sprint Nextel)	[10-digit phone number]@messaging.sprintpcs.com
#                                 [10-digit phone number]@pm.sprint.com (MMS)
#                 Example: 1234567890@messaging.sprintpcs.com
# T-Mobile	                [10-digit phone number]@tmomail.net
#                 Example: 1234567890@tmomail.net
# US Cellular	                [10-digit phone number]email.uscc.net (SMS)
#                                 [10-digit phone number]@mms.uscc.net (MMS)
#                 Example: 1234567890@email.uscc.net
# Verizon	                        [10-digit phone number]@vtext.com
#                                 [10-digit phone number]@vzwpix.com (MMS)
#                 Example: 1234567890@vtext.com
# Virgin Mobile USA	        [10-digit phone number]@vmobl.com
#                 Example: 1234567890@vmobl.com