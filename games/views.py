from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Game
from django.conf import settings
from pathlib import Path
import os
from django.http import FileResponse

def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    # generate file url to render
    file_path = settings.BASE_DIR / "games-list" / f"jeu{game.id}" / f"{game.index}.html"
    
    # Ensure the file exists
    if not file_path.exists():
        raise Http404("Game file does not exist")

    # Read the file content
    with open(file_path, 'r') as file:
        file_content = file.read()

    return HttpResponse(file_content)

def serve_static(request, file_name):
    # get game id from file name
    game_id = lookup_game_id(file_name)
    # Construct the path to the game's static folder
    file_path = settings.BASE_DIR / "games-list" / f"jeu{game_id}" / file_name

    # Security check - prevent directory traversal
    if not os.path.realpath(file_path).startswith(os.path.realpath(settings.BASE_DIR / "games-list" / f"jeu{game_id}")):
        raise Http404("Security error. Access denied.")

    if file_path.exists() and file_path.is_file():
        return FileResponse(open(file_path, 'rb'), as_attachment=False)
    else:
        raise Http404("Requested file does not exist")
    
def list(request):
    games = Game.objects.all()
    return render(request, 'games/list.html', {'games': games})

# methods
def lookup_game_id(file_name):
    # get file name without extension
    file_name = file_name.split(".")[0]
    # get game id from name and model Game
    game = Game.objects.get(index=file_name)
    return game.id