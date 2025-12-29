# TLDR;
- This is a forked repository for my final project in `2026`. [(original)](https://github.com/grammarly/gector)
- This project was tested using Python 3.7.
- I used `Anaconda Prompt (Miniconda3)` to run everything because many of the libraries were `deprecated`
- I modified `requirements.txt` so it can run on my machine using `Miniconda3`.

# PLEASE RUN THIS RIGHT AFTER CLONING THIS REPOSITORY
```.bash
python fix_vocab.py
```

This fixes vocabulary problem by rewriting the file with the correct `next line` delimiter. This file will create a `vocab_backup` folder at the root of the project. Just in case you need to reset the original vocabulary, you can just overwrite the original vocabulary files with the ones in `vocab_backup`.