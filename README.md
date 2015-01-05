Mashdown will split a Youtube mashup video into individual audio files, with documented audio tags.

**Warning**: For Mashdown to work, the video must come with a tracklist listing the start time and track name for each track. The tracklist can either be in the Youtube description or in a local file. Here is a `Youtube video <https://www.youtube.com/watch?v=702dP7vDQhs>`_ that is a perfect candidate.

## Installation

To install Mashdown, you can simply use pip:

```bash
$ pip install mashdown
```

## Usage

```
usage: main.py [-h] [-t TRACKLIST] [-f AUDIOFORMAT] [-o OUTPUT_DIR]
           [--artist ARTIST] [--album ALBUM]
           video

Splits a Youtube mashup video into a list of tagged audio tracks

positional arguments:
  video                 The path, relative or absolute, to the video file

optional arguments:
  -h, --help            show this help message and exit
  -t TRACKLIST, --tracklist TRACKLIST
                        The location of the tracklist. It can either be a
                        Youtube URL or a local path. In the case of a Youtube
                        URL, the tracklist will be extracted from the video
                        description
  -f AUDIOFORMAT, --audioformat AUDIOFORMAT
                        The export audio format. Examples: 'mp3', 'ogg',
                        'mp4', 'flac', ...
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The directory in which the output directory will be
                        created.By default, the current directory will be
                        used.

metadata:
  --artist ARTIST       The artist name
  --album ALBUM         The album name
```

## Example

```bash
    mashdown \
        --tracklist http://www.youtube.com/watch\?v\=702dP7vDQhs \
        --audioformat mp3 \
        --artist "Murray Gold" \
        --album "Doctor Who: Epic Soundtrack Music Mix for 50th Anniversary" \
        ~/dwhelper/Doctor_Who_Epic_Soundtrack_Music_Mix_for_50th_Anniversary_Mu.mp4
```