import os
import sys
import srt
import argparse
from pydub import AudioSegment

def get_slice_indexes(sub):
    '''
    Returns the indexes used to slice the corresponding audio from the subtitle

    Keyword arguments:
    sub - a srt subtitle
    '''
    return int(sub.start.total_seconds() * 1000), int(sub.end.total_seconds() * 1000)


def build_parser():
    '''
    Creates an argparse parser
    '''
    parser = argparse.ArgumentParser(description='Segment .mp3 files according to a provided .srt closed caption file',
                                     prog='srt-parse')

    parser.add_argument('audio_input', type=str,
                        help='Location of .mp3 file to be processed')
    parser.add_argument('srt_input', type=str,
                        help='Location of .srt file to be processed')
    parser.add_argument('--output-dir',  type=str,
                        help='Directory for processed files to be saved to',
                        default='.\\out\\')
    parser.add_argument('--audio-out-file-pattern', type=str,
                        help='A python-style f-string for saving audio files',
                        default='{}-audio.mp3')
    parser.add_argument('--text-out-file-pattern', type=str,
                        help='A python-style f-string for saving text files',
                        default='{}-text.txt')
    parser.add_argument('--output-type', type=str,
                        help='Output filetype',
                        choices=['txt', 'csv'],
                        default='csv')
    parser.add_argument('--csv-seperator', type=str,
                        help='Character sequence used to seperate values in csv',
                        default=',')
    parser.add_argument('--csv-filename', type=str,
                        help='Name of file to write as csv',
                        default='out.csv')
    parser.add_argument('--update-increment', type=int,
                        help='Print progress after every specified amount of segments.',
                        default=25)
    parser.add_argument('--in-encoding', type=str,
                        help='Encoding used to read the .srt file',
                        default='utf-8')
    parser.add_argument('--out-encoding', type=str,
                        help='Encoding to use when writing text data to file',
                        default=None)
    return parser


def write_txt():
    '''
    Write data in .txt format
    '''
    for idx, sub in enumerate(subs):
        if idx % args.update_increment == 0:
            print(f'Processing segment #{idx}')
            
        start, end = get_slice_indexes(sub)
        clip = audio[start:end]
        clip.export(args.output_dir + args.audio_out_file_pattern.format(idx), format='mp3')
        with open(os.path.join(args.output_dir, args.text_out_file_pattern.format(idx)), 'w', encoding=args.out_encoding) as f:
            f.write(sub.content.replace('\n', ' '))


def write_csv():
    '''
    Write data in .csv format
    '''
    with open(os.path.join(args.output_dir, args.csv_filename), 'w', encoding=args.out_encoding) as f:
        for idx, sub in enumerate(subs):
            if idx % args.update_increment == 0:
                print(f'Processing segment #{idx}')
            start, end = get_slice_indexes(sub)
            clip = audio[start:end]
            clip.export(os.path.join(args.output_dir, args.audio_out_file_pattern.format(idx)), format='mp3')
            f.write(args.csv_seperator.join([args.audio_out_file_pattern.format(idx), sub.content.replace('\n', ' ')]))
            f.write('\n')


def get_write_function():
    '''
    Determine which method to use to write to file.
    '''
    write_map = {'txt': write_txt,
                 'csv': write_csv}
    return write_map[args.output_type]


def get_subs():
    '''
    Returns a generator yielding parsed captions from the .srt
    '''
    with open(args.srt_input, 'r', encoding=args.in_encoding) as f:
        str_sub = ''.join(f.readlines())
    return (sub for sub in srt.parse(str_sub))


# Get parser and parse
parser = build_parser()
args = parser.parse_args()

# Error checking
if args.update_increment <= 0:
    parser.error("Update increment must be a postive number")

# Check if output path exists and is a directory
try:
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
except FileExistsError:
    parser.error(f"Output path {args.output_dir} is not a directory.\nsrt-parse will now exit.")
    sys.exit()
 
# Open srt file
subs = get_subs()

# Open audio file
audio = AudioSegment.from_mp3(args.audio_input)

# Determine which writing function to use
write = get_write_function()

# Process audio clips
write()

print('Processing finished!')
