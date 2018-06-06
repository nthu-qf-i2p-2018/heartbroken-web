from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.

@xframe_options_exempt
def index(request):
    return render(request, 'index.html')


def play(request):
    game = Game(
        [AgentRandom('Iron Man'), AgentRandom('Superman'),
         AgentRandom('Batman'), AgentRandom('Spiderman')]
    )

    game.set_game()
    scores = game.play()
