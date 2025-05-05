#!/usr/bin/env python
# Created by Valera at 06.10.2021
# YANDEX BLYADISHE - бля дай исчо
"""
Да не посмотрит этот репозиторий работодатель. Админь.

"""

import logging
import shelve
import pickle
import os
from datetime import datetime

from yandex_music import Client
#from yandex_music.exceptions import Captcha
import click

logging.basicConfig(filename="logging.log", level=logging.INFO)
log = logging.getLogger(__name__)
sdb = shelve.open("shelve.db")


@click.command()
@click.option("-t", "--token", required=True)
@click.option("-df", "--folder-download", default="musics")
def main(token, folder_download):
    numberLastDownloadedTrack = sdb.get("numberLastDownloadedTrack", 0)

    isAuthorize = False

    print("Инициирую клиент для скачки...")
    client = Client(token).init()
    client.request.set_timeout(600)

    print("Капча пройдена! Щя пойдет скачка")
    likedTracks = client.users_likes_tracks()

    for i, track in enumerate(likedTracks):
        try:
            track_id = str(track.id)
            isTrackDownloaded = sdb.get(track_id, False)
            if isTrackDownloaded:
                continue
            # Пока что он как ID фигурирует
            print("####################")
            print(f"Track.id: {track_id}")
            print(f"Track.album_id: {track.album_id}")
            ftchTrack = track.fetch_track()
            track_name = ftchTrack.title
            for x in ftchTrack.artists:
                track_name += " " + x.name
            # Виндоус фишки
            track_name = track_name[:230]
            # Уборка невозможных символов в именах файлов
            track_name = track_name.replace("$", "D")
            track_name = track_name.replace("?", "Q")
            track_name = track_name.replace(":", "T")
            track_name = track_name.replace("/", "S")
            track_name = track_name.replace("\\", "S")
            track_name = track_name.replace('"', "'")
            track_name = track_name.replace('*', "Z")
            track_name = track_name.replace('|', "S")
            track_name = track_name.replace('|', "S")


            print(f"Имя трека: {track_name}")
            print("Загружаю...")
            if not isTrackDownloaded:
                start_time = datetime.now()
                ftchTrack.download(os.path.join(folder_download, f"{numberLastDownloadedTrack} {track_name}.mp3"))
                end_time = datetime.now()
                print('Время загрузки: {}'.format(end_time - start_time))
                sdb[track_id] = True
                sdb.sync()
                with open("Список загруженных треков.txt", "a+") as f:
                    f.write(f"{numberLastDownloadedTrack} {track_name}" + "\n")
                print("Трек загружен!")
        except Exception as e:
            log.exception("При скачке трека он пошел по пизде...")
            with open(f"trackError/{i}.{track_id}.pickle", "w") as f:
                f.write(str(pickle.dumps(track)) + "\r\n")
            with open("Список ID НЕ загруженных треков.txt", "a+") as f:
                f.write(track_id + "\n")
        numberLastDownloadedTrack += 1
        sdb["numberLastDownloadedTrack"] = numberLastDownloadedTrack
        sdb.sync()


if __name__ == "__main__":
    main()