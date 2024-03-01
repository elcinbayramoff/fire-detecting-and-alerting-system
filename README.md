# Fire Detection Project

## Overview

This project focuses on fire detection using the YOLO (You Only Look Once) model. The primary functionality involves detecting fires in webcam or video feeds. When a fire is detected, the corresponding frames are saved in the `detected_images` folder, and an alert email with attached images is sent to a specified target email address.

## Requirements

- Python 3.x
- Dependencies: `ultralytics`, `cvzone`, `cv2`

## Configuration

Before running the project, make sure to configure the following settings in the script:

```bash
# Email configuration
from_email = 'your_email@example.com'  # Replace with your email
to_email = 'target_email@example.com'  # Replace with recipient's email
smtp_server = 'your_smtp_server'  # Replace with your SMTP server
smtp_port = 000  # Replace with your SMTP port
email_password = 'your_email_password'  # Replace with your email password
```
## Contribution
Feel free to contribute by opening issues or submitting pull requests. Any contributions are highly appreciated!
