from setuptools import *

kwargs = {
    "author" : "BrainDisassembly",
    "author_email" : "braindisassm@gmail.com",
    "description" : "Reverse Python Shell",
    "entry_points" : {"console_scripts" : ["revshell=revshell.revshell:main"]},
    "license" : "GPL v3",
    "name" : "revshell",
    "packages" : ["revshell"],
    "version" : "V1.0.0",
}

setup(**kwargs)
