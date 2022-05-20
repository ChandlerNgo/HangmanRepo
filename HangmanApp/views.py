from django.shortcuts import render
import random
# Create your views here.
wordlist = []
with open('HangmanApp/1-1000.txt','r+') as file:
    lines = file.readlines()
    for line in lines:
        updated_line = line[:-1]
        wordlist.append(updated_line)
    
    #remove last letter of word
def index(request):
    letterlist = ""
    if 'answer' not in request.session:
        request.session['guesses'] = []
        answer = random.choice(wordlist)
        answer = answer.upper()
        fillword = "_"*len(answer)
        request.session['answer'] = answer
        request.session['wrong'] = 0
        request.session['fillword'] = fillword
    alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for letters in alphabet_list:
        letterlist += letters +" "
    response = {
        "gamestate": f"static/state{request.session['wrong']}.png/",
        "letterlist": letterlist,
        "word": request.session['answer'],
        "fillword": request.session['fillword'],
    }
    if request.method == "POST":
        if 'confirm' in request.POST:
            guess = request.POST["guess"].upper()
            guesslist = ""
            for letter in request.session['guesses']:
                guesslist = guesslist+letter+" "
            if guess not in alphabet_list:
                response = {
                    "gamestate": f"static/state{request.session['wrong']}.png/",
                    "letterlist": letterlist,
                    "guess": guess,
                    "word": request.session['answer'],
                    "fillword": request.session['fillword'],
                    "error": "Try one of the letters listed above",
                    "guesses":guesslist
                }
            else:# guess is in alphabet_list
                if guess in request.session['guesses']: # you have guessed the letter
                    guesslist = ""
                    for letter in request.session['guesses']:
                        guesslist = guesslist+letter+" "
                    response = {
                        "gamestate": f"static/state{request.session['wrong']}.png/",
                        "letterlist": letterlist,
                        "guess": guess,
                        "word": request.session['answer'],
                        "fillword": request.session['fillword'],
                        "error": "You have guessed this already",
                        "guesses":guesslist
                    }
                else:#you haven't guessed this letter yet
                    request.session['guesses'].append(guess)
                    if guess not in request.session['answer']:
                        if request.session['wrong'] < 6:
                            request.session['wrong'] += 1
                            guesslist = ""
                            for letter in request.session['guesses']:
                                guesslist = guesslist+letter+" "
                            response = {
                                "gamestate": f"static/state{request.session['wrong']}.png/",
                                "letterlist": letterlist,
                                "guess": guess,
                                "word": request.session['answer'],
                                "fillword": request.session['fillword'],
                                "guesses":guesslist
                            }
                        if request.session['wrong'] >= 6:
                            guesslist = ""
                            for letter in request.session['guesses']:
                                guesslist = guesslist+letter+" "
                            response = {
                                "gamestate": f"static/state{request.session['wrong']}.png/",
                                "letterlist": letterlist,
                                "guess": guess,
                                "word": request.session['answer'],
                                "fillword": request.session['answer'],
                                "error": "GAME OVER",
                                "guesses":guesslist
                            }
                            return render(request,"index.html",response)
                    else:
                        for i,wordletter in enumerate(request.session['answer']):
                            if wordletter == guess:
                                temp = list(request.session['fillword'])
                                temp[i] = guess
                                request.session['fillword'] = "".join(temp)
                        if request.session['fillword'] == request.session['answer']:
                            guesslist = ""
                            for letter in request.session['guesses']:
                                guesslist = guesslist+letter+" "
                            response = {
                                "gamestate": f"static/state{request.session['wrong']}.png/",
                                "letterlist": letterlist,
                                "guess": guess,
                                "word": request.session['answer'],
                                "fillword": request.session['fillword'],
                                "error": "YOU WON",
                                "guesses":guesslist
                            }
                        else:
                            guesslist = ""
                            for letter in request.session['guesses']:
                                guesslist = guesslist+letter+" "
                            response = {
                                "gamestate": f"static/state{request.session['wrong']}.png/",
                                "letterlist": letterlist,
                                "guess": guess,
                                "word": request.session['answer'],
                                "fillword": request.session['fillword'],
                                "guesses":guesslist
                            }
                        #update the fillword, guesses
        elif 'reset' in request.POST:
            letterlist = ""
            for letters in alphabet_list:
                letterlist += letters +" "
            answer = random.choice(wordlist)
            answer = answer.upper()
            fillword = "_"*len(answer)
            request.session['answer'] = answer
            request.session['wrong'] = 0
            request.session['fillword'] = fillword
            request.session['guesses'] = []
            guesslist = ""
            for letter in request.session['guesses']:
                guesslist = guesslist+letter+" "
            response = {
                "gamestate": f"static/state{request.session['wrong']}.png/",
                "letterlist": letterlist,
                "word": request.session['answer'],
                "fillword": request.session['fillword'],
                "guesses": guesslist,
            }
    return render(request,"index.html",response)


#create a game over screen and a win screen