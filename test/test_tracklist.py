# encoding: utf-8

"""Test suite of the tracklist module."""


import re
import pytest

from mashdown.tracklist import (
    TRACK_TIME, find_best_match, match_tracklist, tracklist, Track)


@pytest.mark.parametrize('string, expected', [
    ('0:00', {'hours': None, 'minutes': '0', 'seconds': '00'}),
    ('10:00', {'hours': None, 'minutes': '10', 'seconds': '00'}),
    ('0:10:00', {'hours': '0', 'minutes': '10', 'seconds': '00'}),
    ('1:10:00', {'hours': '1', 'minutes': '10', 'seconds': '00'}),
    ('01:10:00', {'hours': '01', 'minutes': '10', 'seconds': '00'}),
    ('10:10:00', {'hours': '10', 'minutes': '10', 'seconds': '00'})
])
def test_track_time_regex(string, expected):
    assert re.search(TRACK_TIME, string).groupdict() == expected


@pytest.mark.parametrize('string, expected', [
    (
        '4. Ballad of Jerry Mono 0:16:41',
        {
            'track_name': u"4. Ballad of Jerry Mono",
            'hours': '0',
            'minutes': '16',
            'seconds': '41'
        }
    ),
    (
        '21:42 The Greatest Story Never Told',
        {
            'track_name': u"The Greatest Story Never Told",
            'hours': None,
            'minutes': '21',
            'seconds': '42'
        }
    ),
])
def test_find_best_match(string, expected):
    assert find_best_match(string).groupdict() == expected


def test_match_tracklist():
    text = u"""00:00 Westminster Bridge
00:17 Doctor Who Theme / Doctor Who Opening Credits / Doctor Who XI
01:10 You're Fired
"""
    matched_tracklist = match_tracklist(text)
    expected = [
        (u"Westminster Bridge", 0),
        (u"Doctor Who Theme / Doctor Who Opening Credits / Doctor Who XI", 17000),
        (u"You're Fired", 70000),
    ]
    assert matched_tracklist == expected


def test_match_tracklist2():
    text = u"""1. Shadows Between the Sky 0:00
2. Inward Journey 3:03
3. Chaos of the Unconscious 8:17
"""
    matched_tracklist = match_tracklist(text)
    expected = [
        (u"1. Shadows Between the Sky", 0),
        (u"2. Inward Journey", 183000),
        (u"3. Chaos of the Unconscious", 497000),
    ]
    assert matched_tracklist == expected


def test_tracklist():
    text = u"""1. Shadows Between the Sky 0:00
2. Inward Journey 3:03
3. Chaos of the Unconscious 8:17
"""
    tl = tracklist(text)
    expected = [
        Track(u"1. Shadows Between the Sky", 0, 183000),
        Track(u"2. Inward Journey", 183000, 497000),
        Track(u"3. Chaos of the Unconscious", 497000, None),
    ]
    assert tl == expected
