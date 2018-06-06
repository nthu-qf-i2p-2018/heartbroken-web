from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from collections import defaultdict
from multiprocessing import Queue
import uuid
import subprocess
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME_DIR = os.path.join(BASE_DIR, 'heart')


move_listen_dict = defaultdict(Queue)
inst_listen_dict = defaultdict(Queue)


def index(request):
    return render(request, 'index.html')


@method_decorator(csrf_exempt, name='dispatch')
def play_post(request):
    if request.method == 'POST':
        if not request.session.get('user-id'):
            request.session['user-id'] = user_id = str(uuid.uuid4())
            subprocess.Popen(['python', 'play.py', user_id], cwd=GAME_DIR)

        play = json.loads(request.body)
        if play:
            move_listen_dict[request.session['user-id']].put(play)

        instruction = inst_listen_dict[request.session['user-id']].get()
        return JsonResponse(instruction)


@method_decorator(csrf_exempt, name='dispatch')
def get_play_post(request):
    if request.method == 'POST':
        instruction = json.loads(request.body)
        # print(instruction)
        user_id = instruction['user_id']
        inst_listen_dict[user_id].put(instruction)
        move = move_listen_dict[user_id].get()
        return JsonResponse(move)
