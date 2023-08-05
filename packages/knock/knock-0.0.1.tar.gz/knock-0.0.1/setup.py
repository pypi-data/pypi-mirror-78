from setuptools import *

kwargs = {
    "author" : "BrainDisassembly",
    "author_email" : "braindisassm@gmail.com",
    "description" : "Trinity's hack emulation into Neo's computer",
    "entry_points" : {"console_scripts" : ["knock=knock.knock:main"]},
    "license" : "GPL v3",
    "name" : "knock",
    "packages" : ["knock"],
    "version" : "V0.0.1",
}

setup(**kwargs)
