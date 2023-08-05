from setuptools import *

kwargs = {
    "author" : "BrainDisassembly",
    "author_email" : "braindisassm@gmail.com",
    "description" : "ARP reconnaissance tool POC",
    "entry_points" : {"console_scripts" : ["pylocalnet=pylocalnet.pylocalnet:main"]},
    "license" : "GPL v3",
    "name" : "pylocalnet",
    "packages" : ["pylocalnet"],
    "version" : "V1.0.0",
}

setup(**kwargs)
