# srt-parse
Segments a .mp3 file into several smaller audio clips using an accompanying .srt closed captioning file.

### Usage

    usage: srt-parse [-h] [--output-dir OUTPUT_DIR]
                     [--audio-out-file-pattern AUDIO_OUT_FILE_PATTERN]
                     [--text-out-file-pattern TEXT_OUT_FILE_PATTERN]
                     [--update-increment UPDATE_INCREMENT]
                     audio_input srt_input

    Segment .mp3 files according to a provided .srt closed caption file

    positional arguments:
      audio_input           Location of .mp3 file to be processed
      srt_input             Location of .srt file to be processed

    optional arguments:
      -h, --help            show this help message and exit
      --output-dir OUTPUT_DIR
                            Directory for processed files to be saved to
      --audio-out-file-pattern AUDIO_OUT_FILE_PATTERN
                            A python-style f-string for saving audio files
      --text-out-file-pattern TEXT_OUT_FILE_PATTERN
                            A python-style f-string for saving text files
      --update-increment UPDATE_INCREMENT
                            Print progress after every specified amount of
                            segments.

### Example
Using `srt-parse`:

    python3 srt-parse.py foo.mp3 foo.srt

Will produce in the following files in the output directory (by default `.\out\`)

    0-audio.mp3
    0-text.txt
    1-audio.mp3
    1-text.txt
    ...
    
One of each file is made per subtitle in the .srt file.
