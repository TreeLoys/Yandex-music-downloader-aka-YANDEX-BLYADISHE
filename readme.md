# YANDEX BLYADISHE 2025
## Yandex music downloader aka YANDEX BLYADISHE 2025
#### ANOTATION
Ну что дружочек, ты решил `скачать музыку в yandex music`?
Или `yandex music download all track`?
Ты попал по адресу!
К твоим услугам надстройка над библиотекой yandex-music-api для скачивания всей музыки с яндекс музыки и поддержания
своей оффлайн библиотеки.

#### HOW IT WORK aka Quick start
Заходи в папушку куда клонирую данный репозиторий `git clone ...`
Получи токен https://yandex-music.readthedocs.io/en/main/token.html затем
.. code:: shell

    $ pip install yandex-music click
    $ python main.py --token "ТОКЕН_СВОЙ"

В следующий раз просто шебани  (в разработке)
.. code:: shell

    $ python main.py --update_discography
    
#### COMMANDS
--login - ваш логин на yanex.music
--password - ваш пароль на yanex.music
--folder-download - путь куда сохранять файлы

#### PROFIT
Теперь у вас есть метод для поддержания своей дискографии с ВК

#### URA, WI ALL IS FUCKED aka ERROR
Не забывай, что у тебя есть капча-шмапча. Попросит ввести просто рядом с прогой открой картинку captcha.png

#### FEATURES
* Ведется журнал названий незагруженных треков
* Можно растянуть загрузку на несколько запусков (да, нажав просто Ctr+C)
* Сохраняет файлы по порядку в начале имени трека "номерПоПорядку_названиеТрека.mp3"
* Запоминает что вы накачали, чтобы добавить новые треки не выкачивая все подряд
* Время загрузки трека

### IT SECUITY?
Вводить пароли безопастно, бо количество буков в readme файле больше чем самого кода)))
Поддается анализу любому питонисту за 30 секунд

#### LICENSE
"THE BEER-WARE LICENSE+" (Revision 3):
<galaktozawr@gmail.com> wrote this files.  As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return. Yandex vozmy menya blyat rabotat.