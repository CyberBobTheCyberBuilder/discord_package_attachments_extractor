# Ce script permet de parcourir une arborescence de fichiers csv, de les décoder, et de récupérer
# dans une liste les liens contenus dans les fichiers csv.
import csv
import os
import sys
import requests
import string
import random

current_dir = os.getcwd()
files_path = "attachments"
# Cette fonction prend une longueur en paramètre et renvoie une chaine de caractères aléatoire de cette longueur comprenant des caractères alphanumériques majuscules et minuscules
def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Fonction qui affiche l'avancement du téléchargement des fichiers
def print_progress(filename, iteration, total, bar_length=100):
    if iteration > 1:
        print ("\033[A                             \033[A")
        print ("\033[A                             \033[A")
        print ("\033[A                             \033[A")
    print("Processing " + filename + "...")
    print("Progress : " + str(iteration * bar_length / total) + "%")
    print("[" + "=" * int((iteration / total) * bar_length) + ">" + " " * (bar_length - int((iteration / total) * bar_length)) + "]")

# Cette fonction permet de décoder un fichier csv de retourner une liste
def decode_csv(file):
    urls = []
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if (len(row) > 3 and row[3] != ''):
                attachements = row[3].split(' ')
                for attachement in attachements:
                    if (attachement.startswith('https://cdn.discordapp')):
                        urls.append(attachement)
    return urls

# Fonction prenant une url en paramètre et télécharge le fichier correspondant et le stocke ensuite dans le dossier "attachments"
def download_file(url, i, t):
    filename = url.split('/')[-1]
    # Si le nom de fichier existe déjà dans attachments, on renomme le fichier
    if (os.path.isfile(files_path + '/' + filename)):
        filename = random_string(10) + '_' + filename
    # print("Processing " + filename + "...")
    print_progress(filename, i, t)
    full_path = os.path.join(files_path, filename)
    try:
        data = requests.get(url)
        # Save file data to local copy
        with open(full_path, 'wb') as file:
            file.write(data.content)
    except Exception as e:
        print(e)

# Fonction principale, on parcourt l'ensemble des dossiers du dossier messages et on décode chaque fichier "channel.csv"
if __name__ == "__main__":
    

    if not os.path.exists(current_dir + "\\" + files_path):
        os.makedirs(current_dir + "\\" + files_path)
        print("Directory " , files_path ,  " Created ")
        
    dirs = os.listdir("messages")
    urls = []
    for dir in dirs:
        if os.path.isdir("messages/" + dir):
            files = os.listdir("messages/" + dir)
            for file in files:
                if file == "messages.csv":
                    urls.extend(decode_csv("messages/" + dir + "/" + file))
    print("Total of " + str(len(urls)) + " urls to download.")
    for url in urls:
        download_file(url, urls.index(url) + 1, len(urls))