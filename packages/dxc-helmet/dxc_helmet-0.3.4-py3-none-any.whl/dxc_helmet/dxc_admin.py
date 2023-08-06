import cv2
import os
import matplotlib.pyplot as plt
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import wget
import shutil

invalid_txt = '''
*****************************************************************************
************    Nothing to display -- invalid image. Try again   ************
*****************************************************************************
'''
try_again_txt = '''
Why not have another go and try another image?
Go back to the "Upload your own image" section
'''

def get_models():
    if not os.path.exists('models'):
        os.mkdir('models')
    else:
        shutil.rmtree('models', ignore_errors=True)
        os.mkdir('models')
    wget.download('https://assets.lbc.co.uk/2016/33/boris-johnson-3-1471423733-view-1.jpg', 'bj.jpg')
    wget.download('https://docs.google.com/uc?export=download&id=16oKgr1RuoUlYcGDqsByiPNa6rnGjhO9T', 'models/deploy.prototxt')
    wget.download('https://docs.google.com/uc?export=download&id=1O0M9K7iGFckmfXrbuGoQU9A_ZdLsUMXP', 'models/res10_300x300_ssd_iter_140000.caffemodel')
    wget.download('https://github.com/jonfernandes/dxc_helmet/raw/master/download/0.1.0/helmet_detector.h5', 'models/helmet_detector.h5')
    print('\nModels downloaded ...')

def check_image(img='image.jpg'):
    img = cv2.imread(img)
    if img is None:
        print(invalid_txt)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img)

def clean_up(image='image.jpg', orig='original_image.jpg'):
    if os.path.exists(image):
        os.remove(image)
    else:
        print(f'{image} does not exist')

    if os.path.exists(orig):
        os.remove(orig)
    else:
        print(f'{orig} does not exist')
    #print('File cleanup completed')

def valid_image(img):
    img = cv2.imread(img)
    if img is None:
        return False
    return True

def get_feedback():
    fromaddr = 'dxchelmet@gmail.com'
    toaddr = 'jonathan.fernandes@dxc.com'
    app = "dkzxdbqjsgznudbm"
    msg = MIMEMultipart() 
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    msg['Subject'] = 'Incorrect helmet classification'
    body = "."
    msg.attach(MIMEText(body, 'plain')) 
    image_file = 'image.jpg'
    original_image = 'original_image.jpg'
    attachment = open(image_file, "rb")
    attachment2 = open(original_image, "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p2 = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read())
    p2.set_payload((attachment2).read()) 
    encoders.encode_base64(p) 
    encoders.encode_base64(p2) 
    p.add_header('Content-Disposition', f"attachment; filename= {image_file}") 
    p2.add_header('Content-Disposition', f"attachment; filename= {original_image}") 
    msg.attach(p) 
    msg.attach(p2)
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, app) 
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text) 
    s.quit()
    print("Thanks - we've sent the image that didn't work across to the team.")
    print(try_again_txt)

def invalid_image(image_file='image.jpg', original_image='original_image.jpg'):
    print(try_again_txt)
    clean_up()
    #print('Environment cleanup')

def valid_file(img):
    if os.path.getsize(img) == 0:
        return False
    return True