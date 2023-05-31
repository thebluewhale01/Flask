'''
    Raspberry Pi GPIO Status and Control
'''
#import RPi.GPIO as GPIO
from flask import Flask, render_template, request, Response
import cv2
#import threading
#import  pyshine as ps

app = Flask(__name__)

server_ip = '127.0.0.1'
port = 9000



#GPIO.setmode(GPIO.BCM
#GPIO.setwarnings(False)
#define sensors GPIOs
button = 20
senPIR = 16
#define actuators GPIOs
ledRed = 13
ledYlw = 19
ledGrn = 26
#initialize GPIO status variables
buttonSts = 0
senPIRSts = 0
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0


def gen():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')

    
@app.route("/")
def index():
    # Read GPIO Status
    buttonSts = button
    senPIRSts = senPIR
    ledRedSts = ledRed
    ledYlwSts = ledYlw
    ledGrnSts = ledGrn
    templateData = {
              'button'  : buttonSts,
              'senPIR'  : senPIRSts,
              'ledRed'  : ledRedSts,
              'ledYlw'  : ledYlwSts,
              'ledGrn'  : ledGrnSts,
          }
    return render_template('index.html', **templateData)


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')     
    
@app.route("/<deviceName>/<action>")#/video_feed")
def action(deviceName, action):
    if deviceName == 'ledRed':
         if action == "on":
              ledRed = 1
              ledYlw = 0
              ledGrn = 0
              button = 0
              #return redirect("/video_feed")
         else:
             ledRed = 0
             ledYlw = 0
             ledGrn = 0
             button = 0
    
    if deviceName == 'ledYlw':
         if action == "on":
              ledRed = 0
              ledYlw = 1
              ledGrn = 0
              button = 0
         else:
             ledRed = 0
             ledYlw = 0
             ledGrn = 0
             button = 0
             
    if deviceName == 'ledGrn':
         if action == "on":
              ledRed = 0
              ledYlw = 0
              ledGrn = 1
              button = 0
         else:
             ledRed = 0
             ledYlw = 0
             ledGrn = 0
             button = 0
    
             
    buttonSts = button
    senPIRSts = senPIR
    ledRedSts = ledRed
    ledYlwSts = ledYlw
    ledGrnSts = ledGrn
   
    templateData = {
             'button'  : buttonSts,
              'senPIR'  : senPIRSts,
              'ledRed'  : ledRedSts,
              'ledYlw'  : ledYlwSts,
              'ledGrn'  : ledGrnSts,
    }
    #return redirect("/video_feed")
    return render_template('index.html',**templateData)
if __name__ == "__main__":
    app.run(debug=True, host=server_ip,port=port+1)