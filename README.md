### About

Splices audio files and obtains their spectrogram

### Run code
* Install requirements: ```sudo pip install requirements.txt```

* Run:
```
python main.py
``` 

* For more customizable runs:
```
python main.py --data_dir=../assets --splices_dir=../assets_splices --specs_dir=../assets_specs --chunk_length_ms=3000 --extension=mp3 --spec_type=log_power
```

* Creates 2 folders:
    * *assets_splices*: audio splices of 3000ms from audio files in *assets* folder
    * *assets_specs*: Log-power spectrograms of each splice
