# httpBackdoor
Linux backdoor written with the HTTPRequestHandler library.

# features
- exfiltrate system information (SSH keys, root users, sys info, etc.)
- command execution (returns the output too)
- can be easily disguised
- lightweight

# how to run on a machine without python being installed
- `pip3 install pyinstaller`
- `pyinstaller --onefile httpBackdoor.py`
- the file in the `dist` directory is your binary that will run on the machine
