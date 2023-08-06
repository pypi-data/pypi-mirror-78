# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radio']

package_data = \
{'': ['*'], 'radio': ['data/*']}

install_requires = \
['click>=7,<8']

entry_points = \
{'console_scripts': ['radio = radio.cli:radio']}

setup_kwargs = {
    'name': 'radio',
    'version': '0.1.3',
    'description': 'Just listen to the radio',
    'long_description': '=====\nradio\n=====\n\n**radio** is a command line tool to **just listen to the radio**.\n\n.. contents::\n\nInstallation\n============\n\n``pip install radio``\n\nor\n\n``pip install --upgrade radio``\n\nUsage\n=====\n\nJust play the radio like this...\n\n``radio play <id>``\n\nLook for available radios with\n\n``radio show``\n\nSearch for you favourite radio with\n\n``radio search <term>``\n\nor else add it with\n\n``radio add <id> --name "My Favourite Radio" --url <streaming-url>``\n\nGeneral usage:\n\n``radio [OPTIONS] COMMAND [ARGS]...``\n\nOptions:\n\n--version  Show the version and exit.\n--help     Show this message and exit.\n\nCommands\n========\n\n:add:     Add or update a radio information.\n:play:    Play a radio.\n:remove:  Remove a radio information.\n:search:  Search radio in the available radios.\n:show:    Show all radios information.\n\nadd\n---\n\nAdd or update a radio information.\n\nUsage:\n\n``radio add [OPTIONS] RADIO_ID``\n\nOptions:\n\n-n, --name TEXT  Radio complete fancy name.  [required]\n-u, --url TEXT   Radio playable streaming url.  [required]\n--help           Show this message and exit.\n\nFor example::\n\n    radio add convos --name "Radio Con Vos FM 89.9" --url https://server1.stweb.tv/rcvos/live/chunks.m3u8\n\nplay\n----\n\nPlay a radio.\n\nUsage:\n\n``radio play [OPTIONS] RADIO_ID``\n\nOptions:\n\n--help  Show this message and exit.\n    \n*Turn off* the radio by pressing "q" or with Ctrl-<C>.\n\nremove\n------\n\nRemove a radio information.\n\nUsage:\n\n``radio remove [OPTIONS] RADIO_ID``\n\nOptions:\n\n--help  Show this message and exit.\n\nsearch\n------\n\nSearch radio in the available radios.\n\nUsage:\n\n``radio search [OPTIONS] STRING``\n\nOptions:\n\n-i, --invert  Invert filter.\n--help        Show this message and exit.\n\nshow\n----\n\nShow all radios information.\n\nUsage:\n\n``radio show [OPTIONS]``\n\nOptions:\n\n--urls   Also show Streaming URLS.\n--count  Show how many radios are available.\n--help   Show this message and exit\n\nHow does it *plays* the radio?\n==============================\n\nIt requires any of the following media player:\n\n- **ffplayer** (ffmpeg package)\n- **cvlc** (vlc package)\n- **mplayer**\n\nPriority or alternative players yet to make *customizable* in future versions.\n\nToDo\n====\n\n- support multiples radio lists (is it useful?)\n- support downloading radio lists from somewhere\n- customize player and priorities or autodetect (something like *rifle* in the *ranger-fm* package)\n- what more?\n- help me at https://github.com/quijot/radio-package\n\nAuthor\n======\n\n* `quijoT <https://github.com/quijot>`_ (Santiago Pestarini <santiagonob@gmail.com>)\n\nCollaborators\n-------------\n\n* `sdeancos <https://github.com/sdeancos>`_ (Samuel de Ancos)\n\nLicense\n=======\n\nradio is licensed under the *do What The Fuck you want to Public License*, WTFPL. See the LICENSE file.\n',
    'author': 'Santiago Pestarini',
    'author_email': 'santiagonob@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quijot/radio-package',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
