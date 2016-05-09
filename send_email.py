import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_ACK(to_addr,name,order_id):

    fromaddr = '<email>'
    toaddrs  = to_addr
    # msg = 'There was a terrible error that occured and I wanted you to know!'

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Acknowledgement - Order No: " + str(order_id)
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    # Create the body of the message (a plain-text and an HTML version).
    text = "Thanks for your interest, You'll receive an email with the estimations soon..."
    html = """\
    <html>
      <head></head>
      <body>
        <h1> <span style="color: #E05D07;">EZ3 </span> <span style="color: #00C09E;"> India </span> </h1>
        <h3> Hello, """ + str(name) + """</h3>
        <h3> We've received your design file, Estimations will be auto-generated and sent to you in less than 5 mins </h3>
        <h5>NOTE: Didn't get the estimation mail? This might be an issue with the model, Reply to this mail for help :) </h5>
        <b>Best,</b><br>
         <b style="color: #E05D07;"> EZ3 </b>
      </body>
    </html>
    """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)


    # Credentials (if needed)
    username = ''
    password = ''

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

def send_estimation(to_addr,time,cost,name,filename,order_id):

    first = os.path.splitext(os.path.basename(filename))[0]
    gcode_Sliced = first + '.gcode'
    path_to_gcode = "http://estimate.ez3.in/uploads/" + gcode_Sliced

    fromaddr = '<email>'
    toaddrs  = to_addr
    # msg = 'There was a terrible error that occured and I wanted you to know!'

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Estimation for Order No: " + str(order_id)
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    # Create the body of the message (a plain-text and an HTML version).
    text = "html disabled?  Time: " + str(time) + "Cost: " + str(cost)
    html = """\
    <html>
      <head></head>
      <body>
        <h1> <span style="color: #E05D07;">EZ3 </span> <span style="color: #00C09E;"> India </span> </h1>
        <h2> Hello, """ + str(name) + """<br>
        <h3>Estimations for your model (""" + str(first) + """) is here!</h3>
        <h3>Time: """ + str(time) + "<br>" +"Cost: &#8377; " + str(cost) + """
        </h3>
        <p><b>Download</b> : <a href=" """ + str(path_to_gcode) +  """  " </a> gcode</p>
        <p> Upload it to <a href="http://gcode.ez3.in">gcode.ez3.in</a> and visualize the layers!</p>
        <b>Best,</b><br>
         <b style="color: #E05D07;"> EZ3 </b>
      </body>
      <h6 style="color: #444"> NOTE: Time & Cost are auto-generated and sometimes vary! </h6>
    </html>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)


    # Credentials (if needed)
    username = ''
    password = ''

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()
