import re

from setuptools import setup

with open('mashdown/__init__.py') as f:
    version = re.search(
        r'(?<=__version__ = \')\d\.\d\.\d(?=\')',
        f.read()
    ).group()


with open('README.rst') as f:
    readme = f.read()

setup(
    name=u'mashdown',
    version=version,
    description=(
        u'Download and split a youtube mashup video in a list of tagged '
        u'audio files'),
    long_description=readme,
    author=u'Balthazar Rouberol',
    author_email=u'brouberol@imap.cc',
    license='License :: OSI Approved :: MIT License',
    packages=['mashdown'],
    install_requires=['pydub', 'pafy', 'mutagen'],
    entry_points={
        'console_scripts': ['mashdown=mashdown.main:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
        'Topic :: Multimedia :: Video :: Conversion'
    ],
    zip_safe=False,
)
