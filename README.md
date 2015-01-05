Mashdown will split a Youtube mashup video into individual audio files, with documented audio tags.

**Warning**: For Mashdown to work, the video must come with a tracklist listing the start time and track name for each track. The tracklist can either be in the Youtube description or in a local file. Here is a [Youtube video](https://www.youtube.com/watch?v=702dP7vDQhs) that is a perfect candidate.

Also, the video must also already be downloaded locally. I recommend using some tools like [DownloadHelper](http://www.downloadhelper.net/) or [youtube-dl](https://github.com/rg3/youtube-dl).

## Installation

To install Mashdown, you can simply use pip:

```bash
$ pip install mashdown
```

## Examples

### Downloading and splitting the mashup
```bash
$ mashdown \
    --audioformat ogg \
    --artist "Murray Gold" \
    --album "Doctor Who: Epic Soundtrack Music Mix for 50th Anniversary" \
    http://www.youtube.com/watch\?v\=702dP7vDQhs
```

### Splitting a local mashup
In this example, the mashup will not be downloaded. The youtube URL is only used to fetch the tracklist information.

```bash
$ mashdown \
    --audioformat ogg \
    --artist "Murray Gold" \
    --album "Doctor Who: Epic Soundtrack Music Mix for 50th Anniversary" \
    --mashupfile path/to/mashupfile
    http://www.youtube.com/watch\?v\=702dP7vDQhs
```

## Usage

```
usage: main.py [-h] [-m MASHUPFILE] [--input-audioformat INPUT_AUDIOFORMAT]
               [-f AUDIOFORMAT] [-o OUTPUT_DIR] [-q] [--artist ARTIST]
               [--album ALBUM]
               url

Split a Youtube mashup video into a list of tagged audio tracks

positional arguments:
  url                   The youtube link to the mashup.

optional arguments:
  -h, --help            show this help message and exit
  -m MASHUPFILE, --mashupfile MASHUPFILE
                        The local path, relative or absolute, to the mashup
                        file.
  --input-audioformat INPUT_AUDIOFORMAT
                        The prefered audio format for the source mashup file.
  -f AUDIOFORMAT, --audioformat AUDIOFORMAT
                        The export audio format. Examples: 'mp3', 'ogg',
                        'mp4', 'flac', ...
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The directory in which the output directory will be
                        created.By default, the current directory will be
                        used.
  -q, --quiet           Remove non important log messages

metadata:
  --artist ARTIST       The artist name
  --album ALBUM         The album name
```

## Dependencies
Mashdown is depends on the following libraries:

- ``pydub`` (which requires ``ffmpeg`` or ``avconv`` to be installed on the system), to cut the video file and export the audio segments
- ``pafy``, to read the Youtube video metadata
- ``mutagen``, to edit the audiofile metadata