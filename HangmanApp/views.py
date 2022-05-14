import re
from django.http import HttpResponse
from django.shortcuts import redirect, render
import random
# Create your views here.

def index(request):
    words = ("enigma","pneumonia","keyboard", "burger", "sheesh", "broken", "brazil", "vietnam")
    letterlist = ""
    if 'guessword' not in request.session:
        guessword = random.choice(words)
        guessword = guessword.upper()
        fillword = "_"*len(guessword)
        request.session['guessword'] = guessword
        request.session['wrong'] = 0
        request.session['fillword'] = fillword
    
    alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for letters in alphabet_list:
        letterlist += letters +" "
    response = {
        "gamestate": f"static/state{request.session['wrong']}.png/",
        "letterlist": letterlist,
        "word": request.session['guessword'],
        "fillword": request.session['fillword'],
    }
    if request.method == "POST":
        if 'confirm' in request.POST:
            guess = request.POST["guess"].upper()
            if guess not in alphabet_list:
                response = {
                    "gamestate": f"static/state{request.session['wrong']}.png/",
                    "letterlist": letterlist,
                    "guess": guess,
                    "word": request.session['guessword'],
                    "fillword": request.session['fillword'],
                    "error": "Try one of the letters listed above"
                }
            else:
                if guess not in request.session['guessword']:
                    response = {
                        "gamestate": f"static/state{request.session['wrong']}.png/",
                        "letterlist": letterlist,
                        "guess": guess,
                        "word": request.session['guessword'],
                        "fillword": request.session['fillword'],
                        "error": "This letter isn't in the word"
                    }
                    if request.session['wrong'] == 6:
                        response = {
                            "gamestate": f"static/state{request.session['wrong']}.png/",
                            "letterlist": letterlist,
                            "guess": guess,
                            "word": request.session['guessword'],
                            "fillword": request.session['fillword'],
                            "error": "GAME OVER"
                        }
                        return render(request,"index.html",response)
                    request.session['wrong'] += 1
                else:
                    response = {
                        "gamestate": f"static/state{request.session['wrong']}.png/",
                        "letterlist": letterlist,
                        "guess": guess,
                        "word": request.session['guessword'],
                        "fillword": request.session['fillword'],
                    }
        elif 'reset' in request.POST:
            words = ("enigma","pneumonia","keyboard", "burger", "sheesh", "broken", "brazil", "vietnam")
            letterlist = ""
            guessword = random.choice(words)
            guessword = guessword.upper()
            fillword = "_"*len(guessword)
            request.session['guessword'] = guessword
            request.session['wrong'] = 0
            request.session['fillword'] = fillword
            response = {
                "gamestate": f"static/state{request.session['wrong']}.png/",
                "letterlist": letterlist,
                "word": request.session['guessword'],
                "fillword": request.session['fillword'],
            }
    return render(request,"index.html",response)