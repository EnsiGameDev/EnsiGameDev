from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from games.models import Game
import zipfile
import os

def upload(request):
    if request.method == 'POST':
        game_folder = request.FILES.get('game_folder')
        game_image = request.FILES.get('game_image')
        action = request.POST.get('action')

        if not game_folder or not game_image:
            return render(request, 'upload.html', {'error': 'Tous les fichiers sont requis.'})

        # Sauvegarder les fichiers
        fs = FileSystemStorage()
        game_foldername = fs.save(game_folder.name, game_folder)
        
         # Créer une instance de Game mais ne pas encore définir le champ `index`
        game = Game(picture=game_image, name='')
        game.save()
        
        # Décompresser le dossier de jeu s'il est en format zip
        game_folder_path = fs.path(game_foldername)
        if game_folder_path.endswith('.zip'):
            # Définir le chemin d'extraction
            game_number = game.id  # Calculer le numéro du jeu
            extract_path = os.path.join(fs.location, 'games-list', f'game{game_number}')
            
            # Créer le dossier d'extraction s'il n'existe pas
            os.makedirs(extract_path, exist_ok=True)
            
            # Extraire le contenu du zip
            with zipfile.ZipFile(game_folder_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    filename = os.path.basename(member)
                    if not filename or filename.startswith('._'):
                        continue  # Ignorer les fichiers ._ et les répertoires
                    source = zip_ref.open(member)
                    target = open(os.path.join(extract_path, filename), "wb")
                    with source, target:
                        target.write(source.read())
            
            # Supprimer le fichier zip après extraction
            os.remove(game_folder_path)
            
            
        game_index = None
        for root, dirs, files in os.walk(extract_path):
            for file in files:
                if file.endswith('.html'):
                    game_index = os.path.splitext(file)[0]
                    break
            if game_index:
                break

        if not game_index:
            return render(request, 'upload.html', {'error': 'Aucun fichier .html trouvé dans le dossier du jeu.'})
        
        game.name=os.path.splitext(game_folder.name)[0]  # Nom du jeu
        game.index = game_index
        game.save()

        # Redirection après traitement
        return redirect('games:list')  # Remplacer 'games_list' par le nom de votre URL de destination

    return render(request, 'upload/upload.html')

def uploaded(request):
    return render(request, 'upload/upload.html')


    