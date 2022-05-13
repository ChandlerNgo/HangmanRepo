from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    import random
    wrong = 0
    words = ("enigma","pneumonia","keyboard", "burger", "sheesh", "broken", "brazil", "vietnam")
    guessword = random.choice(words)
    guessword = guessword.upper()
    wordlength = len(guessword)
    fillword = ""
    guesslist = []
    alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    response = {
        "gamestate": f"static/state{wrong}.png/"
    }
    return render(request,"index.html",response)