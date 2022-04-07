import cv2
from keras.models import load_model
import numpy as np
import time
import random

#read landing page image
landingpage = cv2.imread('files/landingpage2.jpg')

#set up model, camera feed and data array
model = load_model('files/keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#lists of possible choices
choices = ['rock','paper','scissors','null']
#dictionary key-value pairs for {choice x : choice which would defeat x}
dicrps = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
#keep track of scores
humscore = 0
aiscore = 0
#x and y control the text and image of the imshow function below
x = 2
y = 1
#define variables for countdown timer
timerstart = 5
countdown = 5
#define variables for round number and text strings for who wins
round_num = 1
result = ("It's a draw!", "AI wins!", "You win!")
#ires is index of result list
ires = 0
#define choice variables
humchoice, aichoice = "", ""



def rpsround(humchoice):
    global aichoice, ires
    aichoice = random.choice(choices[0:3])
    if humchoice == aichoice:
        ires=0
        return ires
    elif humchoice == dicrps.get(aichoice):
        global humscore
        humscore += 1
        ires = 2
        return humscore, ires
    else:
        global aiscore
        aiscore += 1
        ires = 1
        return aiscore, ires

def start():
        global round_num
        round_num += 1
        rpsround(humchoice)

def mouse(action,a,b, flags, *userdata):
    global x,y
    if action == cv2.EVENT_FLAG_LBUTTON and y==1:    
        if 280 > a > 150 and 375 > b > 350:
            y = 0
            x = 0
   
while True:     
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = model.predict(data)
            result_num = np.where(prediction == np.amax(prediction))
            result_str = choices[int(result_num[1])]
            text = [(f"'s' to start round {round_num} The score is Human:{humscore} Machine: {aiscore}"),
                    (f"Get ready, {int(countdown)}"),
                    "",
                    (f"You played {humchoice}, machine played {aichoice}.{result[ires]} 's' to continue..."),
                    (f"You lose! Human:{humscore} Machine: {aiscore}  Try again? (s) or quit? (q)"),
                    (f"You win! Human:{humscore} Machine: {aiscore}  Try again? (s) or quit? (q)"),
                    (f"Choice wasn't registered, try again (s)")]

            imageText = [frame.copy(),landingpage]    
            font = cv2.FONT_HERSHEY_PLAIN
            color = (255, 255, 255) 
            fontsize = 1
            position = (5, 50)
            
            
            cv2.putText(imageText[y], text[x], position, font, fontsize, color=color)
            cv2.imshow("Rock, Paper, Scissors", imageText[y])
            #on open screen mouse click proceeds to gameplay
            if y == 1:
                cv2.setMouseCallback("Rock, Paper, Scissors", mouse)
            #when s key pressed game, countdown starts
            if cv2.waitKey(1) & 0xFF == ord('s'):
                if x == 0 or x==6:
                    timerstart = time.time()
                    x = 1
                elif x== 3:
                    x=0
                elif x == 4 or x==5:
                    round_num = 1
                    aiscore = 0
                    humscore = 0
                    x = 0
            #q to quit        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            countdown = timerstart-time.time()+5
            if int(countdown) == 0:
                humchoice = choices[int(result_num[1])]
                if humchoice == choices[3]:
                    x=6
                else:
                    start() 
                    timerstart = 5
                    x=3
            #when one player reaches 3, game ends
            if aiscore == 3: 
                    x = 4
            if humscore == 3:
                    x = 5
             
     
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()