import os
import sys
import srt
import argparse
from pydub import AudioSegment


def get_slice_indexes(sub):
    return int(sub.start.total_seconds() * 1000), int(sub.end.total_seconds() * 1000)


parser = argparse.ArgumentParser(description='Segment .mp3 files according to a provided .srt closed caption file',
                                 prog='srt-parse')

parser.add_argument('audio_input', type=str, help='Location of .mp3 file to be processed')
parser.add_argument('srt_input', type=str, help='Location of .srt file to be processed')
parser.add_argument('--output-dir',  type=str, help='Directory for processed files to be saved to',
                    default='.\\out\\')
parser.add_argument('--audio-out-file-pattern', type=str, help='A python-style f-string for saving audio files',
                    default='{}-audio.mp3')
parser.add_argument('--text-out-file-pattern', type=str, help='A python-style f-string for saving text files',
                    default='{}-text.txt')
parser.add_argument('--update-increment', type=int, help='Print progress after every specified amount of segments.',
                    default=25)

args = parser.parse_args()

# Check if output path is real and is a directory
try:
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
except FileExistsError:
    print(f"Output path {args.output_dir} is not a directory.\nsrt-parse will now exit.")
    sys.exit()
    
# Open srt file
with open(args.srt_input, 'r') as f:
    str_sub = ''.join(f.readlines())
subs = (sub for sub in srt.parse(str_sub))

# Open audio file
audio = AudioSegment.from_mp3(args.audio_input)

# Process audio clips
for idx, sub in enumerate(subs):
    if idx % args.update_increment == 0:
        print(f'Processing segment #{idx}')
        
    start, end = get_slice_indexes(sub)
    clip = audio[start:end]
    clip.export(args.output_dir + args.audio_out_file_pattern.format(idx), format='mp3')
    with open(args.output_dir + args.text_out_file_pattern.format(idx), 'w') as f:
        f.write(sub.content.replace('\n', ' '))

print('Processing finished!')

