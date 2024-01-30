from ultralytics import YOLO
import pandas as pd
import os
from datetime import datetime
import shutil
from flask import Flask
from flask_apscheduler import APScheduler
import logging
import sys



#create flask app
app = Flask(__name__)

sched = APScheduler()

class Temp:
    def __init__(self, is_verbose=False):
        # configuring log
        if (is_verbose):
            self.log_level=logging.DEBUG
        else:
            self.log_level=logging.INFO


        log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
        self.log = logging.getLogger(__name__)
        self.log.setLevel(self.log_level)


        # writing to file and console
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.log_level)
        handler.setFormatter(log_format)
        self.log.addHandler(handler)

        # initializing log
        self.log.debug("test")

# Add a new route to the app
@app.route("/")

# Define a new function
def main():


    # specify the img directory path
    path = "/Users/julia/PycharmProjects/PPE_Detection_Yolov8/PPE_Images/"

    # list files in img directory
    files = os.listdir(path)

    if len(files) == 0:
        print("No data to process")

    else:


        for file in files:
            # make sure file is an image
            if file.endswith(('.jpg', 'jpeg')):
                img_path = path + file

        image_strings = [path + str(p) for p in files]

        # Load a model
        model = YOLO('best.pt')  # pretrained YOLOv8n model


        # Run batched inference on a list of images
        results = model.predict(image_strings, save=True, save_txt=True)  # return a list of Results objects

        d=[]
        for result in results:
                boxes = result.boxes  # Boxes object for bbox outputs
                filepath = result.path  # image path
                filename = filepath.rsplit('/', 1)[-1]

                for box in result.boxes:
                    class_id = result.names[box.cls[0].item()]
                    conf = round(box.conf[0].item(), 2)
                    d.append(
                        {
                            'Image Name': filename,
                            'Object type': class_id,
                            'Probability': conf
                        }
                    )
        df=pd.DataFrame(d)
        print(df)

        #save to csv
        currentDateTime = datetime.now().strftime("%m-%d-%Y %H-%M-%S %p")
        df.to_csv('PPE_Detection' + currentDateTime + '.csv', index=False)





        source = "/Users/julia/PycharmProjects/PPE_Detection_Yolov8/PPE_Images/"
        destination = "/Users/julia/PycharmProjects/PPE_Detection_Yolov8/Processed_Images/"

        # gather all files
        allfiles = os.listdir(source)

        # iterate on all files to move them to destination folder
        for f in allfiles:
            src_path = os.path.join(source, f)
            dst_path = os.path.join(destination, f)
            shutil.move(src_path, dst_path)

        # Change os directory back to main file
        os.chdir('/Users/julia/PycharmProjects/PPE_Detection_Yolov8/')

        # converting csv to html
        data = pd.read_csv('PPE_Detection' + currentDateTime + '.csv')






# Run the app
if __name__ == "__main__":
    sched.add_job(id='main', func=main, trigger='cron', hour='00', minute='00', second='00')
    t = Temp(True)
    t.log.debug("test")


    logging.basicConfig(filename='log/flask_apschedulerv6.log')
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)



    sched.start()
    app.run()



