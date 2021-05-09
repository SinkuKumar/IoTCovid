# Python code to illustrate Sending mail from
# your Gmail account
import smtplib

sender_email_id = "doctor.covid.iot.project@gmail.com"
sender_email_id_password = "___________"
receiver_email_id = "chatwithswaraj.sk@gmail.com"

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(sender_email_id, sender_email_id_password)

# message to be sent
message = "Hii Swaraj," \
          "Did you had Breaksaft?"

# sending the mail
s.sendmail(sender_email_id, receiver_email_id, message)

# terminating the session
s.quit()
