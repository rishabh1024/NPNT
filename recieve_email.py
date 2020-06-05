import imaplib
import base64
import os
import email
import base64
from datetime import datetime
from datetime import timedelta

#from apiclient import errors
def recieveEmail():
	email_user = "rishabh@omnipresenttech.com"
	email_pass = "Mrrobot@1024"
	search_criteria = 'REVERSE DATE'
	port = 993
	host = "imap.gmail.com"
	xmail = imaplib.IMAP4_SSL(host,port)

	xmail.login(email_user, email_pass)

	xmail.select('Inbox')
	date_time = datetime.now() - timedelta(days = 1)

	d = date_time.strftime("%d-%b-%Y")
	d = str(d)
	search_mail = '(FROM "artificialintelligenceeco@gmail.com" SINCE "{}")'.format(d)
	type, data = xmail.search(None, search_mail)
	#type, data = xmail.search(None, '(FROM "artificialintelligenceeco@gmail.com" SINCE "04-Jun-2020")')
	#type, data = mail.search(None, 'ALL')
	#type, data = xmail.sort(search_criteria, 'UTF-8', '(FROM "artificialintelligenceeco@gmail.com")')
	mail_ids = data[0]
	id_list = mail_ids.split()

	for msgId in mail_ids.split():
		typ, messageParts = xmail.fetch(msgId, '(RFC822)')
		if typ != 'OK':
			print('Error fetching mail.')
			raise

		emailBody = messageParts[0][1]
		raw_email_string = emailBody.decode('utf-8')
		print(emailBody)
		mail = email.message_from_string(raw_email_string)
		for part in mail.walk():
			if part.get_content_maintype() == 'multipart':
				# print part.as_string()
				continue
			if part.get('Content-Disposition') is None:
				# print part.as_string()
				continue
			fileName = part.get_filename()
			
			if bool(fileName):
				filePath = os.path.join('./', fileName)
				if not os.path.isfile(filePath) :
					print(fileName)
					fp = open(filePath, 'wb')
					fp.write(part.get_payload(decode=True))
					fp.close()
	xmail.close()
	xmail.logout()

recieveEmail() # download the attachement from the email
#os.system('unzip -P 1234 /home/pi/keys.zip') # unzip the attached key file
