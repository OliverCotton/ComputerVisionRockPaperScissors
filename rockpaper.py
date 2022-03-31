import cv2
from keras.models import load_model
import numpy as np
import time
import random
model = load_model('/home/oliver/Documents/rock paper/ComputerVisionRockPaperScissors/ComputerVisionRockPaperScissors/keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

choices = ['rock','paper','scissors','null']
dicrps = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
humscore = 0
aiscore = 0
class rpsgame:

    def rpsround(humchoice):
        aichoice = random.choice(choices)
        #print(aichoice)
        if humchoice == aichoice:
            print("draw")
        elif humchoice == dicrps.get(aichoice):
            global humscore
            humscore += 1
            return humscore
        else:
            global aiscore
            aiscore += 1
            return aiscore
        

            

def start():
        game = rpsgame()
        rpsgame.rpsround(humchoice)


      
      
while True:  
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        result_num = np.where(prediction == np.amax(prediction))
        result_str = choices[int(result_num[1])]
        text = (f"Your choice is {result_str}\npress 's' to submit\nHuman:{humscore} Machine: {aiscore}")
        imageText = frame.copy()
            
        font = cv2.FONT_HERSHEY_PLAIN
        color = (255, 0, 0) # red
        fontsize = 1
    
        position = (50, 50)
        cv2.putText(imageText, text, position, font, fontsize, color=color)
        cv2.imshow("Rock, Paper, Scissors", imageText)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            humchoice = choices[int(result_num[1])]
            print(humchoice)
            start()