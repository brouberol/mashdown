# -*- coding: utf-8 -*-

"""
mashdown.tracklist
~~~~~~~~~~~~~~~~~~

This module contains the extraction functions used to get the tracklist
from different locations (Youtube, local file, etc).

"""

import re

from collections import namedtuple

TRACK_TIME = r'((?P<hours>\d):)?(?P<minutes>\d{2}):(?P<seconds>\d{2})'
TRACK_INFO = r'%s (?P<track_name>[^\n]+)(?=\n+)' % (TRACK_TIME)
Track = namedtuple('Track', ['trackname', 'start_ms', 'end_ms'])


def _start_time_from_groupdict(groupdict):
    """Convert the argument hour/minute/seconds minute into a millisecond value.

    """
    if groupdict['hours'] is None:
        groupdict['hours'] = 0
    return (int(groupdict['hours']) * 3600 +
            int(groupdict['minutes']) * 60 +
            int(groupdict['seconds'])) * 1000


def match_tracklist(text, tracklist_location):
    """Extract a list of traclname/start ms from the text.

    The start time will be converted to milliseconds from the hh:mm:ss
    format.

    """
    track_list = []
    track_list_match = re.finditer(TRACK_INFO, text)
    for track_match in track_list_match:
        start_time = _start_time_from_groupdict(track_match.groupdict())
        track_list.append((track_match.groupdict()['track_name'], start_time))
    if not track_list:
        raise ValueError('No track list could be extracted from %s' % (
            tracklist_location))
    return track_list


def tracklist(text, tracklist_location):
    matched_tracklist = match_tracklist(text, tracklist_location)

    # Compute the end_time from the start_time of the next element
    tracklist = []
    for curr_track, next_track in zip(matched_tracklist, matched_tracklist[1:]):
        track_name, start_time = curr_track
        _, end_time = next_track
        tracklist.append(Track(track_name, start_time, end_time))
    last_trackname, last_track_start_ms = matched_tracklist[-1]
    tracklist.append(Track(last_trackname, last_track_start_ms, None))
    return tracklist


def extract_tracklist(tracklist_location):
    """Extract the tracklist from its location.

    The location can be a local file path or a youtube URL.

    """
    return tracklist(
        tracklist_location.description, tracklist_location.watchv_url)
