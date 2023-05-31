# Welcome to PyShine, this code is for demonstration on PC
# Client can send control commands to server, and also can view live
# video stream on the same webpage.
# We can easily extend this code for Raspberry Pi Zero W and other versions of Pi 

import cv2
import  pyshine as ps #  pip3 install pyshine==0.0.9
import threading
# import RPi.GPIO as io
from flask import Flask, render_template, request
app = Flask(__name__)



FORWARD = 6
BACK = 26
LEFT = 27
RIGHT = 22

map_motion =  {
        FORWARD: "FORWARD",
        BACK : "BACK",
        LEFT : "LEFT",
        RIGHT : "RIGHT"}

server_ip = '127.0.0.1'
port = 9000
HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center><h1> PyShine Live Streaming using OpenCV </h1></center>
<center><img src="stream.mjpg" width='1280' height='960' autoplay playsinline></center>
</body>
</html>
"""

def main():
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = (server_ip,port) # Enter your IP address 
    try:
        StreamProps.set_Mode(StreamProps,'cv2')
        capture = cv2.VideoCapture(0) # replace 'outside.mp4' with 0 depending on webcam id
        capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        capture.set(cv2.CAP_PROP_FPS,30)
        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        server = ps.Streamer(address,StreamProps)
        print('Server started at','http://'+address[0]+':'+str(address[1]))
        server.serve_forever()
        
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()


my_list =[FORWARD,BACK,LEFT,RIGHT]

    
def run_for (pin):
    print(f"action-- {map_motion[pin]}")

def init():
    pass
             
global pin 
pin = FORWARD
init()
@app.route("/", methods=['GET', 'POST'])
def index():
    global pin
    data= 'stop' #default
    if request.method == 'POST':
        data = request.form.get("data")
        if data == 'forward':
            pin = FORWARD
            run_for (pin)
        elif  data == 'back':
            pin = BACK
            run_for (pin)
        elif data == 'left':
            pin = LEFT
            run_for (pin)
        elif data == 'right':
            pin = RIGHT
            run_for (pin)
            print('right')          
        elif data == 'stop':
            print('STOP')
        else:
            return render_template("threading.html")
    elif request.method == 'GET':
        print("NO POST ...")
    return render_template("threading.html")


if __name__ == '__main__':
    
    t1 = threading.Thread(target=main, args=())
    t1.start()
    app.run(debug=True, host=server_ip,port=port+1,threaded=True)
    
