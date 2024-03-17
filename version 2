import random

HANGMAN_PICS = {
    'default': ['''
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
}

words = {
    'animals': 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split(),
    'fruits': 'apple banana orange grape kiwi strawberry pineapple cherry lemon lime pear watermelon grapefruit apricot peach mango'.split(),
    'colors': 'red orange yellow green blue indigo violet black white brown'.split(),
}

def getRandomWord(wordList):
    """
    Returns a random string from the passed list of strings.
    """
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(missedLetters, correctLetters, secretWord, score):
    print()
    print(HANGMAN_PICS['default'][len(missedLetters)])

    print()
    print('Missed letters: ', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')

    print()
    blanks = '_' * len(secretWord)
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    # Display the secret word with spaces between the letters:
    for letter in blanks:
        print(letter, end =' ')
    print()
    print('Current Score:', score)

def getGuess(alreadyGuessed):
    """
    Returns the letter the player entered.
    Ensures the player enters a single letter and nothing else.
    """
    while True:
        print('Please guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Only a single letter is allowed.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a letter from the alphabet.')
        else:
            return guess

def chooseCategory():
    """
    Allows the player to choose a category to play from.
    """
    print('Choose a category:')
    for i, category in enumerate(words.keys(), 1):
        print(f"{i}. {category}")
    while True:
        choice = input()
        if choice.isdigit() and 1 <= int(choice) <= len(words):
            return list(words.keys())[int(choice) - 1]
        else:
            print('Invalid choice. Please enter a number corresponding to the category.')

def calculateScore(secretWord, missedLetters, correctLetters):
    if len(correctLetters) == 0 and len(missedLetters) == 0:  # First guess
        return 1
    score = len(set(correctLetters))  # +1 for every right guess
    if len(missedLetters) == len(HANGMAN_PICS['default']) - 1:  # Game over due to too many wrong guesses
        return 0
    if '_' not in secretWord:  # Complete word guessed
        score += 5
    return score

def playAgain():
    """
    Returns True if the player wants to play again, False otherwise.
    """
    print('Would you like to play again? (y)es or (n)o')
    return input().lower().startswith('y')

def displayHighScores(scores):
    print("High Scores:")
    for score in scores:
        print(score)

def updateHighScores(score, high_scores):
    high_scores.append(score)
    high_scores.sort(reverse=True)
    return high_scores[:5]  # Keep only the top 5 scores

print('|H_A_N_G_M_A_N|')

# Load high scores
try:
    with open("hangman_scores.txt", "r") as file:
        high_scores = [int(score.strip()) for score in file.readlines()]
except FileNotFoundError:
    high_scores = []

# Now for the game itself:
while True:
    category = chooseCategory()
    secretWord = getRandomWord(words[category])
    missedLetters = ''
    correctLetters = ''
    gameIsDone = False

    while True:
        score = calculateScore(secretWord, missedLetters, correctLetters)
        displayBoard(missedLetters, correctLetters, secretWord, score)
        # Let the player enter a letter:
        guess = getGuess(missedLetters + correctLetters)

        if guess in secretWord:
            correctLetters = correctLetters + guess
            # Check to see if the player has won:
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print('You guessed it!')
                print('The secret word is "' + secretWord + '"! You win!')
                score = calculateScore(secretWord, missedLetters, correctLetters)
                high_scores = updateHighScores(score, high_scores)
                gameIsDone = True
        else:
            missedLetters = missedLetters + guess

            # Check if the player has guessed too many times and lost.
            if len(missedLetters) == len(HANGMAN_PICS['default']) - 1:
                displayBoard(missedLetters, correctLetters, secretWord, 0)
                print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                gameIsDone = True

        # If the game is done, ask the player to try again.
        if gameIsDone:
            break

    # Display high scores
    displayHighScores(high_scores)

    # Save high scores
    with open("hangman_scores.txt", "w") as file:
        for score in high_scores:
            file.write(str(score) + "\n")
