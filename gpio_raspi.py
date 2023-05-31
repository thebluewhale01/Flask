'''
    Raspberry Pi GPIO Status and Control
'''
import cv2
import  pyshine as ps
import threading
from flask import Flask, render_template, request
app = Flask(__name__)


server_ip = '127.0.0.1'
port = 9000
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
        #print('Server started at','http://:'+str(address[1]))
        server.serve_forever()
        
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()

@app.route("/")
def index():
   return render_template("index2.html")


if __name__ == '__main__':
    
    t1 = threading.Thread(target=main, args=())
    t1.start()
    app.run(debug=True, host=server_ip,port=port+1,threaded=True)		