# srt-parse
Segments a .mp3 file into several smaller audio clips using an accompanying .srt closed captioning file.

### Usage

    usage: srt-parse [-h] [--output-dir OUTPUT_DIR]
                 [--audio-out-file-pattern AUDIO_OUT_FILE_PATTERN]
                 [--text-out-file-pattern TEXT_OUT_FILE_PATTERN]
                 [--output-type {txt,csv}] [--csv-seperator CSV_SEPERATOR]
                 [--csv-filename CSV_FILENAME]
                 [--update-increment UPDATE_INCREMENT]
                 [--in-encoding IN_ENCODING] [--out-encoding OUT_ENCODING]
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
      --output-type {txt,csv}
                            Output filetype
      --csv-seperator CSV_SEPERATOR
                            Character sequence used to seperate values in csv
      --csv-filename CSV_FILENAME
                            Name of file to write as csv
      --update-increment UPDATE_INCREMENT
                            Print progress after every specified amount of
                            segments.
      --in-encoding IN_ENCODING
                            Encoding used to read the .srt file
      --out-encoding OUT_ENCODING
                            Encoding to use when writing text data to file


### Example
Using `srt-parse`:

    python3 srt-parse.py foo.mp3 foo.srt

Will produce in the following files in the output directory (by default `.\out\`)

    0-audio.mp3
    1-audio.mp3
    2-audio.mp3
    3-audio.mp3
    ...
    out.csv
    
Each file is made per subtitle in the .srt file and out.csv groups each audio file to its transcript.
