# -*- coding: utf-8 -*-

"""
mashdown.metadata
~~~~~~~~~~~~~~~~~

This module contains the masdhown metadata extraction functions.

"""


from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TALB, TPE1

AudioFile = {
    'ogg': OggVorbis,
    'flac': FLAC,
    'mp4': MP4,
}


def write_metadata(audio_format, filepath, title, artist=None, album=None):
    """Write the metadata to the audiofile"""
    if audio_format == 'mp3':
        write_mp3_metadata(filepath, title, artist, album)
    else:
        write_metadata_other_formats(
            audio_format, filepath, title, artist, album)


def write_mp3_metadata(filepath, title, artist, album):
    """Write the metadata to the mp3 file, using the ID3 standard."""
    f = MP3(filepath)
    f['TIT2'] = TIT2(encoding=3, text=[title])
    if artist:
        f['TPE1'] = TPE1(encoding=3, text=[artist])
    if album:
        f['TALB'] = TALB(encoding=3, text=[album])
    f.tags.save()


def write_metadata_other_formats(audio_format, filepath, title, artist, album):
    """Write the metadata to the audio file, which format could be
    anything but mp3.

    """
    f = AudioFile[audio_format](filepath)
    f['title'] = title
    if artist:
        f['artist'] = artist
    if album:
        f['album'] = album
    f.save()
