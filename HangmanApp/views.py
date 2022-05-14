from http.client import HTTPS_PORT
import re
from django.http import HttpResponse
from django.shortcuts import redirect, render
import random
# Create your views here.

def index(request):
    words = ("enigma","pneumonia","keyboard", "burger", "sheesh", "broken", "brazil", "vietnam")
    letterlist = ""
    if 'answer' not in request.session:
        request.session['guesses'] = []
        answer = random.choice(words)
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
        "guesses":request.session['guesses']
    }
    if request.method == "POST":
        if 'confirm' in request.POST:
            guess = request.POST["guess"].upper()
            if guess not in alphabet_list:
                response = {
                    "gamestate": f"static/state{request.session['wrong']}.png/",
                    "letterlist": letterlist,
                    "guess": guess,
                    "word": request.session['answer'],
                    "fillword": request.session['fillword'],
                    "error": "Try one of the letters listed above",
                    "guesses":request.session['guesses']
                }
            else:# guess is in alphabet_list
                if guess in request.session['guesses']: # you have guessed the letter
                    response = {
                        "gamestate": f"static/state{request.session['wrong']}.png/",
                        "letterlist": letterlist,
                        "guess": guess,
                        "word": request.session['answer'],
                        "fillword": request.session['fillword'],
                        "error": "You have guessed this already",
                        "guesses":request.session['guesses']
                    }
                else:#you haven't guessed this letter yet
                    request.session['guesses'].append(guess)
                    if guess not in request.session['answer']:
                        request.session['wrong'] += 1
                        response = {
                            "gamestate": f"static/state{request.session['wrong']}.png/",
                            "letterlist": letterlist,
                            "guess": guess,
                            "word": request.session['answer'],
                            "fillword": request.session['fillword'],
                            "guesses":request.session['guesses']
                        }
                    else:
                        position = request.session['answer'].index(guess)
                        temp = list(request.session['fillword'])
                        temp[position] = guess
                        request.session['fillword'] = "".join(temp)
                        response = {
                            "gamestate": f"static/state{request.session['wrong']}.png/",
                            "letterlist": letterlist,
                            "guess": guess,
                            "word": request.session['answer'],
                            "fillword": request.session['fillword'],
                            "guesses":request.session['guesses']
                        }
                        #update the fillword, guesses
        elif 'reset' in request.POST:
            words = ("enigma","pneumonia","keyboard", "burger", "sheesh", "broken", "brazil", "vietnam")
            letterlist = ""
            for letters in alphabet_list:
                letterlist += letters +" "
            answer = random.choice(words)
            answer = answer.upper()
            fillword = "_"*len(answer)
            request.session['answer'] = answer
            request.session['wrong'] = 0
            request.session['fillword'] = fillword
            request.session['guesses'] = []
            response = {
                "gamestate": f"static/state{request.session['wrong']}.png/",
                "letterlist": letterlist,
                "word": request.session['answer'],
                "fillword": request.session['fillword'],
                "guesses": request.session['guesses'],
            }
    return render(request,"index.html",response)


#create a game over screen and a win screen