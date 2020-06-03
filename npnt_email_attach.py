# Python code to illustrate Sending mail with attachments
# from your Gmail account 
 
# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
  

def sendEmail():
    try:
        timestamp=str(datetime.datetime.now()).split('.')
        tstamp=timestamp[0].split()
        print("Generating Email body..")
        fromaddr = "artificialintelligenceeco@gmail.com"
        toaddr = "rishabh@omnipresenttech.com"
        #toaddr="anjeesh@omnipresenttech.com"
        # instance of MIMEMultipart
        msg = MIMEMultipart()
         
        # storing the senders email address  
        msg['From'] =fromaddr
         
        # storing the receivers email address 
        msg['To'] = toaddr
         
        # storing the subject 
        
        msg['Subject'] = "Check you mail!!"
        # string to store the body of the mail
        body = "Download"
        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
        print("Gathering Image data")
        # open the file to be sent 
        filename = "/home/pi/keys.zip"
        attachment = open(filename, "rb")
        
        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
         
        # To change the payload into encoded form
        p.set_payload((attachment).read())
         
        # encode into base64
        encoders.encode_base64(p)
          
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
         
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
            
            
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
         
        # start TLS for security
        s.starttls()
         
        # Authentication
        s.login(fromaddr, "Ecopark@123")
        print("Logging into server account") 
        # Converts the Multipart msg into a string
        text = msg.as_string()
         
        # sending the mail
        print("Sending Mail")
        s.sendmail(fromaddr, toaddr, text)
        print("Mail Sent")
        # terminating the session
        s.quit()
    except:
        print('Could not send email')
        pass
