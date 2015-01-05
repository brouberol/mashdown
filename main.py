# -*- coding: utf-8 -*-

"""Command line interface to mashdown"""

import argparse
import os
import os.path
import pafy

from mashdown.tracklist import extract_tracklist
from mashdown.audio import AudioExporter


def parse_args():
    parser = argparse.ArgumentParser(
        description=('Splits a Youtube mashup video into a list of '
                     'tagged audio tracks')
    )
    parser.add_argument(
        'video',
        help='The path, relative or absolute, to the video file')
    parser.add_argument(
        '-t', '--tracklist',
        help=('The location of the tracklist. It can either be a Youtube URL '
              'or a local path. In the case of a Youtube URL, the tracklist '
              'will be extracted from the video description'))
    parser.add_argument(
        '-f', '--audioformat',
        default='ogg',
        help=("The export audio format. Examples: 'mp3', 'ogg', 'mp4', "
              "'flac', 'aac', ..."))
    parser.add_argument(
        '-o', '--output-dir',
        default='.',
        help=('The directory in which the output directory will be created.'
              'By default, the current directory will be used.'))

    metadata = parser.add_argument_group('metadata')
    metadata.add_argument('--artist', help='The artist name')
    metadata.add_argument('--album', help='The album name')
    return parser.parse_args()


def main():
    args = parse_args()
    youtube = 'youtube' in args.tracklist
    metadata = {}

    # Get tracklist location
    if youtube:
        video = pafy.new(args.tracklist, basic=False)
        tracklist_location = video
    else:
        tracklist_location = extract_tracklist(args.tracklist)

    # Get metadata
    metadata['artist'] = args.artist
    metadata['album'] = args.album

    # Create the output directory if it does not exist already
    output_dir = os.path.join(
        os.path.abspath(args.output_dir),
        metadata['album'] or os.path.splitext(os.path.basename(args.video))[0]
    )
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Perform the tracklist extraction and audiofile export
    tracklist = extract_tracklist(tracklist_location)
    AudioExporter(
        tracklist=tracklist,
        video_filepath=args.video,
        output_dir=output_dir,
        audio_format=args.audioformat,
        metadata=metadata).export_tracks()

if __name__ == '__main__':
    main()
