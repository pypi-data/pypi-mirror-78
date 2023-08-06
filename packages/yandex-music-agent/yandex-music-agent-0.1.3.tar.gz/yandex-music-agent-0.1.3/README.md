# Yandex Music Agent

Downloads music of selected artists account:

`<artist.title>/<album.year> - <album.title>/<track.num>. <track.title>.mp3`

## Authorization config

`~/YandexMusicAgent/.credentials`

```
[yandex]
login=<user_login>
password=<user_password>
```

## Install with pip
Requires:

* python3 (>=3.7)
* python3-pip

```
pip3 install .
yandex-music-agent -o <target_music_dir>
```

## Run from source
Requires:

* python3 (>=3.7)
* python3-venv

Prepare venv
```
./venv.sh
```
Run main script
```
. venv/bin/activate
PYTHONPATH=src python src/yandex_music_agent/main.py -o <target_music_dir>
```
