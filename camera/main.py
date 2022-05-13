import socket
import base64
import cv2

HOST = '10.0.1.113'
PORT = 5000


class Display:
    data_len = 0
    inidata = None
    data = bytearray()
    msg = None

    def received_data(self, input_data):
        self.inidata = input_data
        d_data = self.inidata.decode('utf-8')
        if d_data.find('len=') == 0:
            f_len = d_data.split('len=')
            self.data_len = int(f_len[1])
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
        if self.msg.find("imaged received") == 0:
            if str(self.data).find("bytearray(b'") == 0:
                data_head_cut = str(self.data).split("bytearray(b'")
                if data_head_cut[1].rfind("')") != -1:
                    data_tail_cut = data_head_cut[1].split("')")
                    image_data = base64.b64decode(data_tail_cut[0])
                    filename = 'Testing.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image_data)
                    output_img = cv2.imread("Testing.jpg", cv2.IMREAD_ANYCOLOR)
                    cv2.imshow("Camera", output_img)
                    self.data.clear()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
camera = Display()
while True:
    data = s.recv(2048)
    msg = camera.received_data(data)
    camera.cut_image()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        s.close()
        break
    if len(data) == 0:  # connection closed
        s.close()
        print('server closed connection.')
        break
