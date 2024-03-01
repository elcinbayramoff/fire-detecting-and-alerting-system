from ultralytics import YOLO
import cvzone
import cv2
import math
import smtplib
import threading
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
# Initialize your YOLO model and other parameters
cap = cv2.VideoCapture(0)
model = YOLO('fire.pt')
classnames = ['fire']
email_status = False
email_lock = threading.Lock()

# Email configuration
from_email = 'Your-email'  # Replace with your email
to_email = 'target-mail'  # Replace with recipient's email
smtp_server = 'smtp-mail.outlook.com'  # Replace with your SMTP server
smtp_port = 000  # Replace with your SMTP port
email_password = 'xxx'  # Replace with your email password
now = datetime.now
# Directory to store images
image_directory = 'detected_images'
os.makedirs(image_directory, exist_ok=True)
now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d %H:%M")
def send_email(image_path):
    subject = 'Fire Alert!'
    body = f'Fire has been detected at {formatted_now}. Please take necessary action.'

    message = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, email_password)

        # Attach the image to the email
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()

        # Create the email message
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain'))
        msg['Subject'] = subject
        msg.attach(MIMEImage(img_data, name=os.path.basename(image_path)))

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    result = model(frame, stream=True)

    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 50:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 + 100],
                                   scale=1.5, thickness=2)

                # Fire detected, save the frame as an image
                image_filename = f'detected_images/fire_{confidence}.png'
                cv2.imwrite(image_filename, frame)

                # Send email with the image attached
                with email_lock:
                    if not email_status:
                        threading.Thread(target=send_email, args=(image_filename,)).start()
                        email_status = True

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
