# this code is to be run somewhere, where you have access to locally run LLMs.
# or can be configured to make API calls to cloud LLMs.


# let's try opening a terminal

import subprocess
import os
command = '../Build.sh'
cwd = 'C++ Development Root/SourceCode'

os.chdir(cwd)
subprocess.run(command)


# note to self
# don't delete entire sourcecode after each run
# check what subprocess you were using last time.
