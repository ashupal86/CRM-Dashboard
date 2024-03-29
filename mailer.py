import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from mimetypes import guess_type
import pdfkit as pdf


# this function create y=the certificate of the user
def certificate_creator():
    html=f"""
    add html data to put in pdf
    """
    file=f"{[ name of pdf]}.pdf"
    pdf.from_string(html, file)
    return file


    

# add file argument in sendMail before commpleting and remove file in SendMail function in bottom 
def sendMail(to_addr,name,domain):
    
    email="add your email here"
    password="generate one time code to access your email thorugh code"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to_addr
    msg['Subject']="Subject of mail"
    your_name=" Add your name here"

    
    content=f"""
<!DOCTYPE html>
<html lang="en">

<body>
  add your mail content here 
  Recomended to write the whole html in a table format
        
    
           
    </body>
</html>
    """
    body = MIMEText(content, 'html')
    
    msg.attach(body)
    file=certificate_creator()
    with open(file, 'rb') as f:
        part = MIMEApplication(f.read(), Name=basename(file))
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(file))
    msg.attach(part)
    
    server.send_message(msg, from_addr=email, to_addrs=[to_addr])

    print(f"Mail Sent to :{to_addr}")




