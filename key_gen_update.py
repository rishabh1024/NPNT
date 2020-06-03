from helpers import create_keys
import os
from datetime import datetime
import datetime as dt
from npnt_email_attach import sendEmail


key_folder = '/home/pi/key_store'
key_name = 'drone'

key_list = os.listdir(key_folder)

pass_word = '1234'

def zip_keys():
	os.system('zip -P {} /home/pi/keys.zip /home/pi/key_store/*.pem'.format(pass_word))

## This function will first creation a pair of keys and then list all files and write the creation time in a text file
def gen_key():
	create_keys(key_folder, key_name)
	f = open("/home/pi/Current_Keys/key_date.txt", "w+")
	key_list = os.listdir(key_folder)
	for i in key_list:
		date = os.path.getctime(os.path.join(key_folder, i))
		print(date)
		f.write(str(datetime.fromtimestamp(date))[:10])
		f.write("\n")
	f.close()
	

if len(key_list) == 0:
	gen_key() # generate the keys
	zip_keys() # zip the keys
	sendEmail() # send the keys to the server
else:
	## If the keys exist it'll first read the creation date of the keys and comare with today's date
	key_update = open("/home/pi/Current_Keys/key_date.txt", "r")
	creation_date = key_update.readline()
	key_update.close()
	creation_date = creation_date.rstrip('\n')
	creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
	expiry_date = creation_date + dt.timedelta(days=90)
	creation_date = creation_date.strftime('%Y-%m-%d')
	expiry_date = expiry_date.strftime('%Y-%m-%d')
	if expiry_date == str(datetime.today().strftime('%Y-%m-%d')):
		print('Keys expired. New keys will be updated')
		os.system('rm /home/pi/Current_Keys/*.pem')
		gen_key() # generate the keys
		zip_keys() # zip the keys
		sendEmail() # send the keys to the server
	else:
		print('Keys not yet expired')
