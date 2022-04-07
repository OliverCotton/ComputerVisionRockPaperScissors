# Computer Vision Rock Paper Scissors
Rock, paper scissors game where player uses hand gestures to play versus the computer.
Uses python 3.8 (with cv2, keras, numpy, time and random modules).

## Contents
1. Project milestones
2. Project files

## 1. Project Milestones

### 1.1 Milestone 1: Coded logic of rock, paper, scissors game
Put together a simple rock paper scissors game object with which a human player can play rock paper scissors against the computer. 

The machine choice is randomly selected from a list of rock, paper and scissors:
    `aichoice = random.choice(rpsgame.choices)`
The player is asked to input 0, 1 or 2 to choose between rock, paper and scissors:
    `humchoice = rpsgame.choices[int(input("0 for rock, 1 for paper, 2 for scissors"))]`

A dictionary `dicrps` stores the pairs of rock, paper and scissors with the key-value pair representing a hand gesture and the hand gesture which defeats it respectively:
`rpsgame.dicrps = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}`

`if, elif, else` statements within the `rpsround()` function check if the computer and human chose the same gesture (a draw), or if the human choice is the same as the value of the key matching the machine's choice (in which case, the human wins). if neither of these conditions are met then by process of elimnation the machine must win.
    if humchoice == aichoice:
                print("draw")
            elif humchoice == rpsgame.dicrps.get(aichoice):
                rpsgame.humscore += 1
            else:
                rpsgame.aiscore += 1

The game continues until one player reaches a score of 5, at which point the game ends:
    `while rpsgame.humscore < 5 and rpsgame.aiscore < 5:
                    self.rpsround(self)
                print(f'Human got {rpsgame.humscore}, AI got {rpsgame.aiscore}')`

The full script is below:

    `import random
    class rpsgame:


        def __init__(self):
            rpsgame.choices = ['rock','paper','scissors']
            rpsgame.dicrps = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
            rpsgame.humscore = 0
            rpsgame.aiscore = 0
            rpsgame.text = (f"Human: {rpsgame.humscore} Machine: {rpsgame.humscore}")

            


        def rpsround(self):
            aichoice = random.choice(rpsgame.choices)
            
            humchoice = rpsgame.choices[int(input("0 for rock, 1 for paper, 2 for scissors"))]
            if humchoice == aichoice:
                print("draw")
            elif humchoice == rpsgame.dicrps.get(aichoice):
                rpsgame.humscore += 1
            else:
                rpsgame.aiscore += 1

            print(rpsgame.humscore, rpsgame.aiscore)

        def play(self):
            while rpsgame.humscore < 5 and rpsgame.aiscore < 5:
                self.rpsround(self)
            print(f'Human got {rpsgame.humscore}, AI got {rpsgame.aiscore}')

    def start():
            game = rpsgame()
            rpsgame.play(rpsgame)

    if __name__ == '__main__':
        start()`

### 1.2 Milestone 2: Trained computer vision model
Using the teachable machines standard image model tool ([teachable machines](https://teachablemachine.withgoogle.com/train/image)), I trained a model to recognise a rock, paper or scissors hand gesture as well as a null input. Around 1000 images were used of each category, generated using the record webcam function on teachable machines.

This code was used to interact with the model, to produce an opencv window and predict what the hand gesture the player is making:
    
    `import cv2
    from keras.models import load_model
    import numpy as np
    import time
    model = load_model('/home/oliver/Documents/rock paper/ComputerVisionRockPaperScissors/ComputerVisionRockPaperScissors/keras_model.h5')
    cap = cv2.VideoCapture(0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)



    while True: 
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        cv2.imshow('frame', frame)
        # Press q to close the window
        print(prediction)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()`


### 1.3 Milestone 3: Integrated Milestones 1 & 2
The two scripts were combined, the model's most likely result replaced the keyboard input used in milestone 1. 

### 1.4 Milestone 4: User Interface
Functions were added such that through hand gestures, keyboard and mouse input, the player can navigate the game and play to a best of 3 against the computer. The program interacts with the user mostly through the `cv2.putText()` function. There is a list of text items (`text`):
    
    `text = [(f"'s' to start round {round_num} The score is Human:{humscore} Machine: {aiscore}"),
                        (f"Get ready, {int(countdown)}"),
                        "",
                        (f"You played {humchoice}, machine played {aichoice}.{result[ires]} 's' to continue..."),
                        (f"You lose! Human:{humscore} Machine: {aiscore}  Try again? (s) or quit? (q)"),
                        (f"You win! Human:{humscore} Machine: {aiscore}  Try again? (s) or quit? (q)"),
                        (f"Choice wasn't registered, try again (s)")]`
    
The `putText()` function looks like this:
     cv2.putText(imageText[y], text[x], position, font, fontsize, color=color)

Events such as mouse clicks, or keyboard inputs modify the value of `x` (the index of the `text` list), such as in this example:
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
                    if x == 0 or x==6:
                        timerstart = time.time()
                        x = 1
                    elif x== 3:
                        x=0
                    elif x == 4 or x==5:
                        round_num = 1
                        aiscore = 0
                        humscore 

Depending on the current value of `x`, the s key will start the countdown timer, progress to a different round of the game or restart the game with fresh scores:

The player is then lead by text instructions which are presented at the top of the screen:
![text instructions](screenshot.png)

Rather than using `putText`, `cv2.Overlay` could be used to overlay graphics telling the player the score, indicating what they had selected etc - however this slowed the framerate and the production of professional looking graphics was beyond the scope of this project, and so this aproach was eventually rejected.

Similarly the variable `y` alters the image opencv presents in the window, between a landing page introducing the player to the game, and the feed from the webcam refreshed in a while loop. 

The player is first greeted with a landing page indicating how to use the program:
![landing page](landingpage2.jpg)

This code handles the mouse click event:
    
    #y == 1 is when the landing page is the active view
    if y == 1:
                cv2.setMouseCallback("Rock, Paper, Scissors", mouse)
    
---- This calls the mouse() function:

    def mouse(action,a,b, flags, *userdata):
        global x,y
        if action == cv2.EVENT_FLAG_LBUTTON and y==1:
            if 280 > a > 150 and 375 > b > 350:
                y = 0
                x = 0

The if the left mouse button is pressed mouse() in the coordinates of the 'click here' text, the global values of x and y are updated. This takes the player to the webcam veiw with text which prompts them to play.


## 2. Project files
`rockpaper.py` - this python script runs the game. It calls `keras_model.h5` for the teachable machines model, and `landingpage2.jpg` for the game landing page. 
`screenshot.png` - a screenshot of the text instructions 