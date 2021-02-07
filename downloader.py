import os
from datetime import datetime
from pytube import YouTube
from pytube import Playlist

DOWNLOAD_DIR = 'D:\\Videoclips\\'
RESOLUTION = '720p'

def download_playlist(playlist_url):
    pl = Playlist(playlist_url)
    print('Baixando playlist: ' + pl.title)
    playlist_dir = get_or_create_playlist_dir(pl.title)

    for video in pl.videos:
        try:
            if not exist_video_in_dir(video.title):
                vid = video.streams.filter(
                    progressive=True, 
                    file_extension='mp4').order_by('resolution').desc().first()
            
                if vid:
                    vid.download(output_path=playlist_dir)
            else:
                print('O video {} ja existe no diretorio {}'.format(video.title, playlist_dir))

        except Exception as error:
            print('Ocorreu um erro ao realizar download do video ', video)

    print('Videos baixados com sucesso...')


def get_or_create_playlist_dir(playlist_name):
    directory = os.path.join(DOWNLOAD_DIR, playlist_name) 

    if not os.path.exists(directory):
        os.mkdir(directory)
        print('diretorio {} criado com sucesso..'.format(directory))

    return directory

''' Verifica se o video já existe no diretorio '''
def exist_video_in_dir(video_title):
    videos = os.listdir(DOWNLOAD_DIR)
    list_video_titles = []

    for video in videos:
        name =  os.path.splitext(video)[0]
        list_video_titles.append(name)
    
    return True if video_title in list_video_titles else False


if __name__ == "__main__":
    start_time = datetime.now()
    playlist = 'https://www.youtube.com/watch?v=CWyOJjoinJ0&list=PLQGx8UJi4WExC7F3MTYiBWk07DAIg_asD'
    download_playlist(playlist)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))