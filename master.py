from set_env import set_env
from log_handler import open_log_file, close_log_file, print_log_msg



log_file_name = "fire_proj_main"
old_stdout, log_file = open_log_file(log_file_name)

set_env(required = {"twilio", "gps",
                "picamera", "tensorflow",
                "numpy", "matplotlib",
                "opencv-contrib-python",
                "keras", "pillow",
                "scipy"},
        req_env = ['email', 'email_password',
            'twillio_sid', 'twillio_auth_token',
            'phone', 'messaging_service_sid'],
        logfile = log_file_name)



## Uncomment these imports before running on Rasberry-Pi
# import picamera
from time import time, sleep
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from email_message import send_email_message, get_recievers
from model_maker import make_model
# from GPS_Capture import getPositionData



## Function for detecting fire in image
def parse_image(image_for_testing, model):
    print_log_msg("Computing result from image...")
    test_image=image.load_img(image_for_testing,target_size=(224,224))
    test_image=image.img_to_array(test_image)
    test_image=test_image/255
    test_image=np.expand_dims(test_image,axis=0)
    result=np.argmax(model.predict(test_image),axis=1)
    print_log_msg("Result of image: ", result)
    return result



# This function is for running the entire project on Rasberry-Pi
def run_on_pi():
    with picamera.PiCamera() as camera:
        camera.resolution = (256, 256)
        camera.framerate = 80
        camera.start_preview()
        sleep(1)

        start = time()
        for filename in camera.capture_continuous('./testFolder/image{timestamp:%H:%M:%S.%f}.jpg'):
            prediction = parse_image(filename,my_model)
            finish = time()
            print_log_msg('Captured %s at %.2ffps' % (filename, 1 / (finish - start)))
            print_log_msg("Sending email and message...")
            send_email_message(lat_lon=getPositionData(),
                            receivers=get_recievers(),
                            warning_level=prediction)
            print_log_msg("Email and message sent.")
            sleep(0.1)
            start = time()



## Check if model exists, if not create it
if not os.path.exists(os.path.join(os.getcwd(), 'Image_Classifier.h5')):
    print_log_msg("Making Model...")
    make_model()
    print_log_msg("Model Completed.")

print_log_msg("Loading Model...")
my_model = load_model("./Image_Classifier.h5")
print_log_msg("Model Loaded.")

## Uncomment in Rasberry-Pi, does not run in other os's
# run_on_pi()


## Test Code
send_email_message(lat_lon= (45, 45),
                receivers=get_recievers(),
                warning_level=parse_image('fire.jpg',my_model))

close_log_file(old_stdout, log_file)
