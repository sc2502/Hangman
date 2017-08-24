import random
import Tkinter
import csv
import sys

# TO ADD:
# HIGH SCHORE: can see high scores, writes correctly
# NEW GAME: text changes so used can see new theme and such

wordList = open("C:\Python27\Scripts\wordList.csv")
csv_wordList = csv.reader(wordList)

wordBox = {}
global themes
themes = []
for row in csv_wordList:
    themes.append(row[0])
    wordBox[row[0]] = row[1:]

global finished
finished = False
answer = ""


def resetAnswer(right_before):
    global w_guess
    w_guess = [""]
    global t_guess
    t_guess = []
    global theme
    repeat = True
    global pastAnswer
    global finished
    finished = False
    pastAnswer.append(right_before)
    r = 1
    n = 0
    while repeat is True:
        theme = themes[random.randint(0, len(themes) - 1)]
        answerN = random.choice(wordBox[theme])
        for past in pastAnswer:
            if past == answerN:
                repeat = True
                r = 15
                n += 1
        if r is not 15:
            repeat = False
        if len(pastAnswer) == len(wordBox) * 11:
            repeat = False
            pastAnswer = []
        r = 1

    global answer
    answer = answerN


global pastAnswer
pastAnswer = []
resetAnswer("")


class MenuBar(Tkinter.Menu):
    def newGame(self):
        #self.scores()
        global pastAnswer
        pastAnswer = []
        resetAnswer("")
        global score
        score = 0
        global q
        q = 0
    def quits(self): sys.exit()

    def scores(self):
        print("one day we'll have high scores...")
        #app = GUI_scores(None)
        #app.title('High Scores')
        #app.mainloop()

    def __init__(self, parent):
        Tkinter.Menu.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        fileMenu = Tkinter.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="New Game", underline=1, command=self.newGame)
        fileMenu.add_command(label="See Scores", underline=1, command=self.scores)
        fileMenu.add_command(label="Exit", underline=1, command=self.quits)


class GUI(Tkinter.Tk):
    def __init__(self, parent):
        global score
        score = 0
        global q
        q = 0
        global maxTurns
        maxTurns = 6
        global pastAnswer
        pastAnswer = []
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.initialize()

    def initialize(self):
        man = 7
        bot = man + 7
        self.grid()

        # type guess box
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)  # enter guess
        self.entry.grid(column=0, row=bot, sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set("Type guess")

        # submit guess button
        submit = Tkinter.Button(self, text=u"Click Here or Press Enter",
                                command=self.OnButtonClick)
        submit.grid(column=1, row=bot)

        # New Game button
        play_again = Tkinter.Button(self, text=u"Next Word", command=self.nextMatch)
        play_again.grid(column=0, row=bot + 2, columnspan=2)

        # Hangman, guesses (Rules on startup)
        self.labelVariable = Tkinter.StringVar()
        gLabel = Tkinter.Label(self, textvariable=self.labelVariable, anchor="w")
        gLabel.grid(column=0, row=0, columnspan=2)
        self.labelVariable.set(self.showRules(maxTurns) +
                               "\n\n" + self.printSpace())

        # GUI Options
        self.grid_columnconfigure(0, weight=1)  # column moves with resize
        self.grid_rowconfigure(0, weight=1)  # row moves with resize
        self.resizable(False, True)  # horizontal,vertical
        self.update()
        self.geometry("300x300")  # GUI size #HxV
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def nextMatch(self):  # restart game with new random answer
        global w_guess
        global t_guess
        resetAnswer(answer)
        self.labelVariable.set(self.showRules(maxTurns) +
                               "\n\n" + self.printSpace())

    def OnButtonClick(self):
        self.entry.focus()
        self.entry.selection_range(0, Tkinter.END)
        guess = self.entryVariable.get()  # get guess
        self.labelVariable.set(self.checkGuess(guess))  # update Hangman,guesses

    def OnPressEnter(self, event):
        self.entry.focus()
        self.entry.selection_range(0, Tkinter.END)
        guess = self.entryVariable.get()  # get guess
        self.labelVariable.set(self.checkGuess(guess))  # update Hangman,guesses

    # display Rules of hangman on start up
    def showRules(self, maxTurns):
        global score
        rules = str("Hello, welcome to hangman!\n" +
                    "You get " + str(maxTurns) + " incorrect guesses. " +
                    "\nGuess in letters only." +
                    "\n Your score is: ") + str(score)
        return rules

    # print the man
    def printMan(self):
        global w_guess
        global answer
        numWrong = len(w_guess)
        if numWrong > 7: numWrong = 8
        body = "O"
        arm = " -"
        leg1 = " /"
        leg2 = "\\"
        head = "  o\n"
        hat1 = "  ____ \n" + "  |  | \n" + " -----\n"
        hat2 = "hat\n"
        hat = hat2
        man = [" ", hat, head, arm, body, arm + "\n", leg1, leg2]
        deadman = ""
        if numWrong > 1:
            for x in range(0, numWrong):
                deadman += man[x]
        if numWrong > 7:
            global score
            score -= len(answer)
            deadman = "GAME OVER\n YOU SUCK! \n" + deadman + "\n The answer was: " + answer
            # pastAnswer.append(answer)
        return deadman

    # print _ or the correctly guessed letter
    def printSpace(self):
        global t_guess
        global answer
        global score
        bar = ""
        cor = 0
        length = len(t_guess)
        for i in answer:  # loop each letter
            no = 0
            for g in t_guess:  # loop check letter against guess
                if i != g:
                    no += 1
            if no == length:  # if no == length then blankspace
                bar += "_ "
            else:
                cor += 1
                bar = bar + i.upper() + " "
        if cor == len(answer):
            global q

            if q < 1:
                global score
                score += len(answer)

            q = 1
            bar += "\n\n GAME OVER YOU WON!"
        bar += "\n\n Theme: " + theme
        return bar

    # check user guess against word
    def checkGuess(self, guess):
        global answer
        global t_guess
        correct = False
        guess = guess.lower()
        t_guess.append(guess)  # always add on
        for letter in answer:  # check guess against each letter in answer
            if letter == guess:
                correct = True
                break
            else:
                correct = False
        if not correct:
            global w_guess
            w_guess.append(guess)
            # make ouputtext nicer
            guessed = w_guess[1].upper()
            for p in w_guess[2:]:
                guessed = guessed + ", " + p.upper()
            w_guess[0] = guessed
        # text to be updated: hangman, correct/incorrect guesses
        text = str("\n\n" + self.printMan() + "\n" + self.printSpace() +
                   "\n\n You have incorrectly guessed: " + str(w_guess[0]) +
                   "\n\n Your score is:" + str(score))
        return text


# running program
if __name__ == "__main__":
    # play game
    app = GUI(None)
    app.title('Hangman')
    app.mainloop()
