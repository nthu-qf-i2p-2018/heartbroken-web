from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from collections import defaultdict
from multiprocessing import Queue
import subprocess
import logging
import uuid
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
        data = json.loads(request.body)
        if not (data and request.session.get('user-id')):
            request.session['user-id'] = user_id = str(uuid.uuid4())
            logging.info('Start a game with user {}'.format(user_id))
            subprocess.Popen(['python', 'play.py', user_id], cwd=GAME_DIR)
        else:
            move_listen_dict[request.session['user-id']].put(data)

        instruction = inst_listen_dict[request.session['user-id']].get()
        if instruction['instruction'] == 'end':
            del inst_listen_dict[request.session['user-id']]
        return JsonResponse(instruction, status=instruction.get('status', 200))


@method_decorator(csrf_exempt, name='dispatch')
def get_play_post(request):
    if request.method == 'POST':
        instruction = json.loads(request.body)
        # print(instruction)
        user_id = instruction['user_id']
        inst_listen_dict[user_id].put(instruction)

        if instruction['instruction'] == 'end':
            move = {}
            del move_listen_dict[user_id]
        else:
            move = move_listen_dict[user_id].get()
        return JsonResponse(move)
