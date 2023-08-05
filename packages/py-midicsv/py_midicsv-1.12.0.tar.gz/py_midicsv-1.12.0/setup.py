# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_midicsv', 'py_midicsv.midi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-midicsv',
    'version': '1.12.0',
    'description': 'A library for converting MIDI files from and to CSV format',
    'long_description': '# py_midicsv\n\n[![CircleCI](https://circleci.com/gh/timwedde/py_midicsv.svg?style=svg)](https://circleci.com/gh/timwedde/py_midicsv)\n[![Downloads](https://pepy.tech/badge/py-midicsv)](https://pepy.tech/project/py-midicsv)\n\nA Python library inspired by the [midicsv](http://www.fourmilab.ch/webtools/midicsv/) tool created by John Walker. Its main purpose is to bidirectionally convert between the binary `MIDI` format and a human-readable interpretation of the contained data in text format, expressed as `CSV`.  \nIf you found this library, you probably already know why you need it.\n\n\n## Disclaimer\n\nThis library is currently in Beta. This means that the interface might change and that the encoding scheme is not yet finalised. Expect slight inconsistencies.\n\n\n## Installation\n\n`py_midicsv` can be installed via pip:\n```bash\n$ pip install py_midicsv\n```\n\nAlternatively you can build the package by cloning this repository and installing via [poetry](https://github.com/sdispater/poetry):\n```bash\n$ git clone https://github.com/timwedde/py_midicsv.git\n$ cd py_midicsv/\n$ poetry install\n```\n\n\n## Usage\n\n```python\nimport py_midicsv as pm\n\n# Load the MIDI file and parse it into CSV format\ncsv_string = pm.midi_to_csv("example.mid")\n\n# Parse the CSV output of the previous command back into a MIDI file\nmidi_object = pm.csv_to_midi(csv_string)\n\n# Save the parsed MIDI file to disk\nwith open("example_converted.mid", "wb") as output_file:\n    midi_writer = pm.FileWriter(output_file)\n    midi_writer.write(midi_object)\n```\n\n## Differences\n\nThis library adheres as much as possible to how the original library works, however generated files are not guaranteed to be entirely identical when compared bit-by-bit.  \nThis is mostly due to the handling of meta-event data, especially lyric events, since the encoding scheme has changed. The original library did not encode some of the characters in the Latin-1 set, while this version does.\n',
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timwedde/py_midicsv',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
