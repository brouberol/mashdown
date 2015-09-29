# -*- coding: utf-8 -*-

"""Command line interface to mashdown"""

import argparse
import os
import os.path
import pafy

from mashdown.tracklist import tracklist
from mashdown.audio import AudioExporter


def parse_args():
    parser = argparse.ArgumentParser(
        description=('Split a Youtube mashup video into a list of '
                     'tagged audio tracks'))
    parser.add_argument(
        'url',
        help='The youtube link to the mashup.')
    parser.add_argument(
        '-m', '--mashupfile',
        help='The local path, relative or absolute, to the mashup file.')
    parser.add_argument(
        '--input-audioformat',
        default='mp4',
        help='The prefered audio format for the source mashup file.')
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
    metadata = {}
    args = parse_args()

    def log(msg):
        if not args.quiet:
            print(msg)

    log('Fetching metadata for %s...' % (args.url))
    youtube_page = pafy.new(args.url, basic=False)

    if not args.mashupfile:
        # Downloading mashup
        log('Downloading mashup file from %s' % (args.url))
        bestaudio = youtube_page.getbestaudio(preftype=args.input_audioformat)
        if not bestaudio:
            log('Could not find any %s audio file' % (args.input_audioformat))
            bestaudio = youtube_page.getbestaudio()
        log('Downloading %s' % (bestaudio.url))
        mashupfile = os.path.abspath(bestaudio.download(quiet=args.quiet))
    else:
        mashupfile = os.path.abspath(args.mashupfile)

    # Get metadata
    metadata['artist'] = args.artist
    metadata['album'] = args.album

    # Create the output directory if it does not exist already
    output_dir = os.path.join(
        os.path.abspath(args.output_dir),
        metadata['album'] or os.path.splitext(
            os.path.basename(mashupfile))[0]
    )
    if not os.path.exists(output_dir):
        log('Creating ' + output_dir)
        os.makedirs(output_dir)

    # Perform the tracklist extraction and audiofile export
    log('Extracting track information...')
    tracks = tracklist(youtube_page.description)

    log('Exporting and tagging audio files...')
    AudioExporter(
        tracklist=tracks,
        video_filepath=mashupfile,
        output_dir=output_dir,
        audio_format=args.audioformat,
        metadata=metadata).export_tracks()

    # Cleaning up (only if the file was downloaded in the first place)
    if not args.mashupfile:
        os.unlink(mashupfile)

if __name__ == '__main__':
    main()
