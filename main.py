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
        '-m', '--mashup',
        required=True,
        help=('The path to the video file. It can either be a Youtube link or '
              'a local path, absolute or relative.'))
    parser.add_argument(
        '-f', '--audioformat',
        default='ogg',
        help=("The export audio format. Examples: 'mp3', 'ogg', 'mp4', "
              "'flac', ..."))
    parser.add_argument(
        '-o', '--output-dir',
        default='.',
        help=('The directory in which the output directory will be created.'
              'By default, the current directory will be used.'))
    parser.add_argument(
        '-q', '--quiet', action='store_true', default=False,
        help=('Remove non important log messages'))

    metadata = parser.add_argument_group('metadata')
    metadata.add_argument('--artist', help='The artist name')
    metadata.add_argument('--album', help='The album name')
    return parser.parse_args()


def main():
    args = parse_args()

    def log(msg):
        if not args.quiet:
            print(msg)

    metadata = {}

    # Get tracklist location
    log('Fetching metadata for %s...' % (args.mashup))
    if 'youtube' in args.mashup:
        video = pafy.new(args.mashup, basic=False)
        bestaudio_url = video.getbestaudio(preftype='mp4').url
        mashupfile = bestaudio_url.download(quiet=args.quiet)
    else:
        mashupfile = os.path.abspath(args.mashup)

    # Get metadata
    metadata['artist'] = args.artist
    metadata['album'] = args.album

    # Create the output directory if it does not exist already
    output_dir = os.path.join(
        os.path.abspath(args.output_dir),
        metadata['album'] or os.path.splitext(os.path.basename(args.video))[0]
    )
    if not os.path.exists(output_dir):
        log('Creating ' + output_dir)
        os.makedirs(output_dir)

    # Perform the tracklist extraction and audiofile export
    log('Extracting track information...')
    tracklist = extract_tracklist(mashupfile)

    log('Exporting and tagging audio files...')
    AudioExporter(
        tracklist=tracklist,
        video_filepath=args.video,
        output_dir=output_dir,
        audio_format=args.audioformat,
        metadata=metadata).export_tracks()

if __name__ == '__main__':
    main()
