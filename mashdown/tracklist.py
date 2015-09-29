# -*- coding: utf-8 -*-

"""
mashdown.tracklist
~~~~~~~~~~~~~~~~~~

This module contains the extraction functions used to get the tracklist
from different locations (Youtube, local file, etc).

"""

import re

from collections import namedtuple

TRACK_TIME = r'((?P<hours>\d{1,2}):)?(?P<minutes>\d{1,2}):(?P<seconds>\d{2})'
TRACK_INFO = [
    r'%s (?P<track_name>.+)' % (TRACK_TIME),
    r'(?P<track_name>.+) %s' % (TRACK_TIME),
]
Track = namedtuple('Track', ['trackname', 'start_ms', 'end_ms'])


def _start_time_from_groupdict(groupdict):
    """Convert the argument hour/minute/seconds minute into a millisecond value.

    """
    if groupdict['hours'] is None:
        groupdict['hours'] = 0
    return (int(groupdict['hours']) * 3600 +
            int(groupdict['minutes']) * 60 +
            int(groupdict['seconds'])) * 1000


def find_best_match(line):
    matches = []
    for pattern in TRACK_INFO:
        match = re.match(pattern, line)
        if match:
            matches.append(match)
    if not matches:
        return None
    return sorted(matches, key=lambda m: len(m.group()), reverse=True)[0]


def match_tracklist(text):
    """Extract a list of trackname/start ms from the text.

    The start time will be converted to milliseconds from the hh:mm:ss
    format.

    """
    track_list = []
    for line in text.split('\n'):
        track_match = find_best_match(line)
        if not track_match:
            continue
        start_time = _start_time_from_groupdict(track_match.groupdict())
        track_list.append((track_match.groupdict()['track_name'], start_time))
    return track_list


def tracklist(text):
    matched_tracklist = match_tracklist(text)
    if not matched_tracklist:
        raise ValueError('No track list could be extracted.')

    # Compute the end_time from the start_time of the next element
    tracklist = []
    for curr_track, next_track in zip(matched_tracklist, matched_tracklist[1:]):
        track_name, start_time = curr_track
        _, end_time = next_track
        tracklist.append(Track(track_name, start_time, end_time))
    last_trackname, last_track_start_ms = matched_tracklist[-1]
    tracklist.append(Track(last_trackname, last_track_start_ms, None))
    return tracklist
