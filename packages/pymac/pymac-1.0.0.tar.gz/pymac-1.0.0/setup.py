from setuptools import *

kwargs = {
    "author" : "BrainDisassembly",
    "author_email" : "braindisassm@gmail.com",
    "description" : "PyMac 1.0.0 [Python MAC Adress Changer]",
    "entry_points" : {"console_scripts" : ["pymac=pymac.pymac:main"]},
    "license" : "GPL v3",
    "name" : "pymac",
    "packages" : ["pymac"],
    "version" : "V1.0.0",
}

setup(**kwargs)
