import socket
import base64
import cv2

HOST = '10.0.1.113' #Please input the IP the connected PICO device
PORT = 5000 #Input the Port number for connecting the PICO device

class Display:
     """Interface to gathering and manage the data received from the PICO side
     - Please refer to the ov2640 pico tcp test.py for more information
     - Data will be combine back together by using "received_data" 
     - cut_image is cutting not related data for saving the image
     - Used opencv to load the image 
    """
    data_len = 0
    inidata = None
    data = bytearray()
    msg = None

    def received_data(self, input_data):
        """Function: Receiving and combining the data into a base64 encoded message
        :param byte input_data: the data received from Pico device
        :param str msg (return): Sending message back to the receving data status
        """        
        self.inidata = input_data
        d_data = self.inidata.decode('utf-8')
        if d_data.find('len=') == 0: # first received msg will be the length of the image
            f_len = d_data.split('len=') 
            self.data_len = int(f_len[1]) #remove unwanted data counting purpose
            print(self.data_len)
            self.msg = "processing"
        else:
            if self.data_len > 2048:
                self.data_len = self.data_len - 2048
                self.data.extend(self.inidata)
                self.msg = "processing"
            elif self.data_len > 0:
                self.data_len = 0
                self.data.extend(self.inidata)
                self.msg = "imaged received"
                print(self.data)
        return self.msg

    def cut_image(self):
        """Remove all the unwanted message from the terminal side
        - The message required to required to change to str to remove unwanted msg
        - Decode the base64 msg back to byte
        - Save the image into jpg format
        - display the image by using opencv's imshow
        """
        if self.msg.find("imaged received") == 0: #check the data receving status
            if str(self.data).find("bytearray(b'") == 0: #cut all the unwanted information
                data_head_cut = str(self.data).split("bytearray(b'")
                if data_head_cut[1].rfind("')") != -1:
                    data_tail_cut = data_head_cut[1].split("')")
                    image_data = base64.b64decode(data_tail_cut[0]) #decode the msg back to bytes
                    filename = 'Testing.jpg' #file name
                    with open(filename, 'wb') as f:
                        f.write(image_data) #save it 
                    output_img = cv2.imread("Testing.jpg", cv2.IMREAD_ANYCOLOR) #collect the image by using imread
                    cv2.imshow("Camera", output_img) # using imshow to show the image
                    self.data.clear() #clear the unwatned information

#socket for communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
camera = Display()
while True: 
    data = s.recv(2048) #receoved data
    msg = camera.received_data(data) #combine the data
    camera.cut_image() #show the image
    if cv2.waitKey(1) & 0xFF == ord('q'): #turn off the display and the connection with pico
        s.close()
        break
    if len(data) == 0:  # connection closed
        s.close()
        print('server closed connection.')
        break
