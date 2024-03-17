import tkinter as tk
from tkinter import messagebox
import random
import webbrowser

HANGMAN_PICS = ['''
    +---+
         |
         |
         |
        ===''', '''
    +---+
    O   |
        |
        |
       ===''', '''
    +---+
    O   |
    |   |
        |
       ===''', '''
    +---+
    O   |
   /|   |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
   /    |
       ===''', '''
    +---+
    O   |
   /|\  |
   / \  |
       ===''']

words = {
    'Animals': 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split(),
    'Fruits': 'apple banana orange grape kiwi strawberry pineapple cherry lemon lime pear watermelon grapefruit apricot peach mango'.split(),
    'Colors': 'red orange yellow green blue indigo violet black white brown'.split(),
}

class HangmanGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        
        self.secret_word = ""
        self.missed_letters = ""
        self.correct_letters = ""
        self.current_pic_idx = 0
        self.points = 0
        
        self.category_var = tk.StringVar()
        self.category_var.set("Animals")
        self.prev_category = "Animals"
        
        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        # Category selection
        category_frame = tk.Frame(self.master)
        category_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        category_label = tk.Label(category_frame, text="Select Category:")
        category_label.pack(side="left")
        category_menu = tk.OptionMenu(category_frame, self.category_var, *words.keys(), command=self.on_category_change)
        category_menu.pack(side="left", fill="x", expand=True)

        # Hangman picture display
        self.hangman_label = tk.Label(self.master, text=HANGMAN_PICS[0], font=("Courier", 12))
        self.hangman_label.grid(row=1, column=0, padx=10, pady=5)

        # Secret word display
        self.secret_word_label = tk.Label(self.master, text="", font=("Arial", 20, "bold"))
        self.secret_word_label.grid(row=2, column=0, padx=10, pady=5)

        # Missed letters display
        self.missed_letters_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.missed_letters_label.grid(row=3, column=0, padx=10, pady=5)

        # Points display
        self.points_label = tk.Label(self.master, text="Points: 0", font=("Arial", 12))
        self.points_label.grid(row=4, column=0, padx=10, pady=5)

        # Letter buttons
        letters_frame = tk.Frame(self.master)
        letters_frame.grid(row=5, column=0, padx=10, pady=5)
        self.letter_buttons = []
        for i in range(26):
            letter = chr(ord('a') + i)
            btn = tk.Button(letters_frame, text=letter.upper(), width=3, command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=i // 7, column=i % 7, padx=2, pady=2)
            self.letter_buttons.append(btn)

        # Restart button
        restart_button = tk.Button(self.master, text="Restart Game", command=self.new_game)
        restart_button.grid(row=6, column=0, padx=10, pady=5)

    def on_category_change(self, *args):
        if self.category_var.get() != self.prev_category:
            self.prev_category = self.category_var.get()
            self.new_game()

    def new_game(self):
        self.secret_word = getRandomWord(words[self.category_var.get()])
        self.missed_letters = ""
        self.correct_letters = ""
        self.current_pic_idx = 0
        self.update_points(0)

        self.update_display()

    def guess_letter(self, letter):
        if letter in self.missed_letters or letter in self.correct_letters:
            messagebox.showinfo("Hangman", "You have already guessed this letter.")
            return

        if letter in self.secret_word:
            self.correct_letters += letter
            self.update_points(10)  # Add points for correct guess
        else:
            self.missed_letters += letter
            self.current_pic_idx += 1

        self.update_display()

    def update_display(self):
        # Ensure current_pic_idx doesn't go beyond the range of HANGMAN_PICS
        if 0 <= self.current_pic_idx < len(HANGMAN_PICS):
            # Update hangman picture
            self.hangman_label.config(text=HANGMAN_PICS[self.current_pic_idx])
        else:
            print("Error: current_pic_idx out of range")

        # Update missed letters
        self.missed_letters_label.config(text="Missed Letters: " + ", ".join(self.missed_letters))

        # Update secret word display
        displayed_word = " ".join([letter if letter in self.correct_letters else "_" for letter in self.secret_word])
        self.secret_word_label.config(text=displayed_word)

        # Check for win/lose condition
        if all(letter in self.correct_letters for letter in self.secret_word):
            self.end_game(True)
        elif self.current_pic_idx == len(HANGMAN_PICS) - 1:
            self.end_game(False)

    def update_points(self, points):
        self.points += points
        self.points_label.config(text="Points: " + str(self.points))

    def end_game(self, win):
        self.master.quit()  # Quit Tkinter main loop

        if win:
            messagebox.showinfo("Game Over", "You win!")
        else:
            messagebox.showinfo("Game Over", f"Game Over! The correct word was: {self.secret_word}")
        
        video_path = "win.mp4" if win else "lost.mp4"  # Path to the video for win or lose scenario

        # Open the video in the default web browser
        webbrowser.open(video_path)

def getRandomWord(wordList):
    return random.choice(wordList)

def main():
    root = tk.Tk()
    hangman_game = HangmanGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
