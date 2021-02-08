import os
import ffmpy
import re
from datetime import datetime
from pytube import YouTube
from pytube import Playlist

DOWNLOAD_DIR = 'D:\\Videoclips\\'

PLAYLISTS_URL = [
    'https://www.youtube.com/watch?v=kkg9fmrZ_Lk&list=PLwnxR295e2u6Dn-30Fi0H-8WTBUa0Tx8B'
    #'https://www.youtube.com/watch?v=VpJKsoMWnZM&list=PLipAo7Mf9fxsjTq_lX6XD6dNdcHXfVK1H', # funk 2021
    #'https://www.youtube.com/watch?v=gUpGTRR4Tt4&list=PLB8HqqmpyIBcAHYt_w15AprSLViIGrToO', # reggae brasileiro
    #'https://www.youtube.com/watch?v=4b9_5xzAuSU&list=RDGMEMHDXYb1_DDSgDsobPsOFxpA', # Mix hip hop
    #'https://www.youtube.com/watch?v=YrQLmElRT-E&list=PL7V1hXWh2rMr4pz6lCkzHMHMLU3-BfQ2S' # Melhores tribo
]

''' Realiza o download de uma determinada playlist '''
def download_playlist(playlist_url):
    start_time = datetime.now()
    pl = Playlist(playlist_url)

    if len(pl) == 0:
        print('A playlist {} não contém videos'.format(playlist_url))
        return

    print('Baixando playlist: ' + pl.title)
    
    playlist_dir = get_or_create_playlist_dir(pl.title)

    for video in pl.videos:
        try:
            if not exist_video_in_dir(playlist_dir, video.title):
                vid = video.streams.filter(
                    progressive=True, 
                    file_extension='mp4').order_by('resolution').desc().first()

                print('Baixando video {}'.format(vid.title))

                if vid:
                    vid.download(output_path=playlist_dir)
                
        except Exception as error:
            print('Ocorreu um erro ao realizar download do video ', video)
            continue

    end_time = datetime.now()
    print('Videos da playlist: {} baixados com sucesso...'.format(pl.title))
    print('Duration: {}'.format(end_time - start_time))


def get_or_create_playlist_dir(playlist_name):
    pl_name = re.sub('[!,*)@#%(&$_?.^|]', '', playlist_name)
    playlist = pl_name.replace(' ', '-')
    directory = os.path.join(DOWNLOAD_DIR, playlist) 

    if not os.path.exists(directory):
        os.mkdir(directory)
        print('diretorio {} criado com sucesso..'.format(directory))

    return directory


''' Verifica se o video já existe no diretorio '''
def exist_video_in_dir(playlist_dir, video_title):
    videos = os.listdir(playlist_dir)
    list_video_titles = []

    for video in videos:
        name =  os.path.splitext(video)[0]
        list_video_titles.append(name)

    return True if video_title in list_video_titles else False


if __name__ == "__main__":
    
    for playlist in PLAYLISTS_URL:
        try:
            download_playlist(playlist)
        except Exception as error:
            print('Ocorreu um erro ao realizar download da playlist: ', playlist)
            print(error)
            continue