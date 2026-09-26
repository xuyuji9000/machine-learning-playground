``` shell
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

whisper sample1.flac --model tiny

ls ~/.cache/whisper/
```

<!-- Reference -->

[sound track sample]: https://huggingface.co/spaces/speechbox/whisper-restore-punctuation/resolve/main/sample1.flac