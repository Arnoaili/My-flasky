from config import config
import smtplib
from email.mime.text import MIMEText

mail = config['default']

def send_email(to_list, subject, user):
    content = "User '%s' has joined !" % user
    me = "li.ai" + "@" + mail.mail_postfix
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = to_list
    try:
        server = smtplib.SMTP()
        server.connect(mail.mail_host)  
        server.login(mail.mail_user,mail.mail_pass) 
        server.sendmail(me, to_list, msg.as_string())
        server.quit()
        return True
    except Exception, e:
        print str(e)
        return False

