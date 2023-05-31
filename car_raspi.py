import  pyshine as ps #  pip3 install pyshine==0.0.9
import threading
#import RPi.GPIO as io
#import picamera
from flask import Flask, render_template, request

app = Flask(__name__)

FORWARD = 6
BACK = 26
LEFT = 27
RIGHT = 22

server_ip = '192.168.10.1'
port = 9000

map_motion =  {FORWARD: "FORWARD",
        BACK : "BACK",
        LEFT : "LEFT",
        RIGHT : "RIGHT"}

HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center><h1> PyShine Live Streaming using OpenCV </h1></center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
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



def init():
    io.cleanup()
    io.setmode(io.BCM)              
    io.setup(FORWARD,io.OUT)  
    io.setup(BACK,io.OUT)
    io.setup(LEFT,io.OUT)
    io.setup(RIGHT,io.OUT)

def run_for (pin):
    print(f"action-- {map_motion[pin]}")
    #io.cleanup()
    #io.setmode(io.BCM)
    #io.setup(pin, io.OUT)
    low()
    io.output(pin, io.HIGH)


def forward():
    print(f"action-- {map_motion[pin]}")
    init()
    io.output(6, io.LOW)
    io.output(26, io.HIGH)
    io.output(27, io.HIGH)
    io.output(22, io.LOW)

def backward():
    print(f"action-- {map_motion[pin]}")
    init()
    io.output(6, io.HIGH)
    io.output(26, io.LOW)
    io.output(27, io.LOW)
    io.output(22, io.HIGH)

def left():
    print(f"action-- {map_motion[pin]}")
    init()
    io.output(6, io.HIGH)
    io.output(26, io.LOW)
    io.output(27, io.HIGH)
    io.output(22, io.LOW)

def right():
    print(f"action-- {map_motion[pin]}")
    init()
    io.output(6, io.LOW)
    io.output(26, io.HIGH)
    io.output(27, io.LOW)
    io.output(22, io.HIGH)

def stop():
    print(f"action-- STOP")
    init()
    io.output(6, io.LOW)
    io.output(26, io.LOW)
    io.output(27, io.LOW)
    io.output(22, io.LOW)    

global pin 
pin = FORWARD
#init()
@app.route("/", methods=['GET', 'POST'])

def index():
    
    global pin
    data= 'stop'
    if request.method == 'POST':
        data = request.form.get("data")
        
        if data == 'forward':
            pin = FORWARD
            forward()
        elif  data == 'back':
            run_for(BACK)
            pin = BACK
        elif data == 'left':
            run_for(LEFT)
            pin = LEFT
        elif data == 'right':         
            run_for(RIGHT)
            pin = RIGHT
        elif data == 'stop':
            io.setmode(io.BCM)
            io.setup(pin, io.OUT)
            io.output(pin, io.LOW)
            io.cleanup()

        else:
            return render_template("index.html")
    elif request.method == 'GET':
        print("NO POST ...")
    return render_template("index.html")


if __name__ == '__main__':
    
    t1 = threading.Thread(target=main, args=())
    t1.start()
    app.run(debug=True, host=server_ip,port=port+1,threaded=True)
    
