#!/usr/bin/env python
# Created by Valera at 06.10.2021
# YANDEX BLYADISHE - бля дай исчо
"""Да не посмотрит этот репозиторий работодатель."""

import logging
import shelve
import pickle
import os
from yandex_music import Client
from yandex_music.exceptions import Captcha
import click
MUSICS_PATH = "D:\yandexMusics"
logging.basicConfig(filename="logging.log", level=logging.INFO)
log = logging.getLogger(__name__)

sdb = shelve.open("shelve.db")


@click.command()
@click.option("-l", "--login", required=True)
@click.option("-p", "--password", required=True)
@click.option("-df", "--folder-download", default="musics")
def main(login, password, folder_download):
    numberLastDownloadedTrack = sdb.get("numberLastDownloadedTrack", 0)

    isAuthorize = False

    print("Инициирую клиент для скачки...")
    client = None
    captcha_key = None
    captcha_answer = None
    while not isAuthorize:
        try:
            client = Client.from_credentials(login, password, captcha_answer, captcha_key)
            isAuthorize = True
        except Captcha as e:
            print("Ощибка! Капчу запросило зло!")
            e.captcha.download('captcha.png')
            os.system("captcha.png")
            captcha_key = e.captcha.x_captcha_key
            captcha_answer = input('Число с картинки: ')
    if client is None:
        print("Почему-то нет авторизации, все пошло по пизде. Выхожу. ")
        exit(-1)

    print("Капча пройдена! Щя пойдет скачка")
    likedTracks = client.users_likes_tracks()

    for i, track in enumerate(likedTracks[numberLastDownloadedTrack:]):
        with open("listDownloadedTrack.txt", "a+") as f:
            f.write(str(pickle.dumps(track)) + "$$ENDOBJTRACK$$")
        # Пока что он как ID фигурирует
        print("####################")
        print(f"Track.id: {track.id}")
        print(f"Track.album_id: {track.album_id}")
        track_id = str(track.id)
        try:
            ftchTrack = track.fetch_track()
            track_name = ""
            isTrackDownloaded = sdb.get(track_id, False)
            print("fetch_track() успех! Трек не загружен. Начинаю загрузку.")
            if not isTrackDownloaded:
                ftchTrack.download(folder_download+f"/{numberLastDownloadedTrack}_{track_name}.mp3")
                sdb[track_id] = True
                sdb.sync()
                print("Трек загружен!")
            else:
                print(f"Warning!{track.id} Трек уже сохранен в базе!")
        except Exception as e:
            log.exception("При скачке трека он пошел по пизде...")
            with open(f"trackError/{i}.{track_id}.pickle", "w") as f:
                f.write(str(pickle.dumps(track)) + "\r\n")
            with open("listDownloadedTrack.txt", "a") as f:
                f.write(f"$$ERRORNOTDOWNLOADED$${track_id}")
        sdb["numberLastDownloadedTrack"] = numberLastDownloadedTrack
        sdb.sync()
        # Новая строка на трек
        with open("listDownloadedTrack.txt", "a") as f:
            f.write("\r\n")


if __name__ == "__main__":
    main()