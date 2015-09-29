# -*- coding: utf-8 -*-

"""
mashdown.audio
~~~~~~~~~~~~~~

This module contains the export functions that will split the mashup
video file to independants tagged and named audio files.

"""

import pydub
import re

from os.path import join

from mashdown.metadata import write_metadata


class AudioExporter(object):

    def __init__(
        self,
        tracklist,
        video_filepath,
        output_dir,
        audio_format,
        metadata
    ):
        self.tracklist = tracklist
        self.video_filepath = video_filepath
        self.output_dir = output_dir
        self.audio_format = audio_format
        self.metadata = metadata
        self.extension = video_filepath.split('.')[-1]
        self.audiofile = pydub.AudioSegment.from_file(
            video_filepath, self.extension)
        self.nb_tracks = len(tracklist)

    def export_tracks(self):
        for i, track in enumerate(self.tracklist):
            self.export_track(track, i + 1)

    def export_track(self, track_info, track_nb):
        name, start, end = track_info
        name = name.replace('/', '-').strip().lstrip('-').strip()
        # Strip any numerical index/prefix, to avoid any redundancy
        name = re.sub(r'\d+[.-]\s?', '', name)
        if end is None:
            audiosegment = self.audiofile[start:]
        else:
            audiosegment = self.audiofile[start:end]
        filename = '%s - %s.%s' % (
            # we need to make sure that there is an appropriate amount of '0' as
            # suffix, in order to always have the tracks playing the the right
            # order
            str(track_nb).zfill(len(str(self.nb_tracks))),
            name,
            self.audio_format)
        filepath = join(self.output_dir, filename)
        print(filepath)
        audiosegment.export(filepath, format=self.audio_format)
        write_metadata(
            audio_format=self.audio_format,
            filepath=filepath,
            title=name,
            artist=self.metadata['artist'],
            album=self.metadata['album'])
