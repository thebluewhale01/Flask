from flask import Flask, render_template, request, Response
import cv2
#import RPi.GPIO as GPIO

ledRed = 13
app = Flask(__name__)
server_ip = '127.0.0.1'
port = 9000

'''def gen():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')'''

@app.route('/')
def index():
   return render_template("pin.html")

'''@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame') '''

@app.route("/pinstatus", methods=['POST'])
def pinstatus():
    if request.form['lighton']:
        '''GPIO.setmode(GPIO.BOARD)
        GPIO.setup(3, GPIO.OUT)
        GPIO.output(3, GPIO.LOW)'''
        GPIO = 1


    if request.form['lightoff']:
        '''GPIO.setmode(GPIO.BOARD)
        GPIO.setup(3, GPIO.OUT)
        GPIO.output(3, GPIO.HIGH)'''
        GPIO = 0
    


    


if __name__ == "__main__":
   #app.run(debug=True)
   app.run(debug=True, host=server_ip,port=port+1)