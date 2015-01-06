Mashdown will download and split a Youtube mashup video into individual audio files, with documented audio tags.

**Warning**: For Mashdown to work, the video must come with a tracklist listing the start time and track name for each track. The tracklist can either be in the Youtube description or in a local file. Here is a `Youtube video <https://www.youtube.com/watch?v=upzOSSQWSYU>`_ that is a perfect candidate.


Installation
============

To install Mashdown, you can simply use pip:

.. code-block:: bash

  $ pip install mashdown


Examples
========

Downloading and splitting the mashup
------------------------------------

.. code-block:: bash

    $ mashdown \
        --audioformat ogg \
        --album "The Lord of the Rings Sountrack" \
        --artist "Howard Shore" \
        https://www.youtube.com/watch\?v\=upzOSSQWSYU


Splitting a local mashup
------------------------
In this example, the mashup will not be downloaded. The youtube URL is only used to fetch the tracklist information.

.. code-block:: bash

    $ mashdown \
        --audioformat ogg \
        --mashupfile path/to/mashupfile
        --album "The Lord of the Rings Sountrack" \
        --artist "Howard Shore" \
        https://www.youtube.com/watch\?v\=upzOSSQWSYU


Usage
=====

..

    usage: mashdown [-h] [-m MASHUPFILE] [--input-audioformat INPUT_AUDIOFORMAT]
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


Dependencies
============

Mashdown is depends on the following libraries:

- ``pydub`` (which requires ``ffmpeg`` or ``avconv`` to be installed on the system), to cut the video file and export the audio segments
- ``pafy``, to download the Youtube video and get its metadata
- ``mutagen``, to edit the audiofile metadata