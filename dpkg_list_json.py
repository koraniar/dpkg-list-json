#!/usr/bin/env python3

# MIT License

# Copyright (c) 2019 Anurag Dulapalli

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
import sys

def getSoftwareWithGUI():
    lines = os.popen('dpkg --search "*.desktop" | awk "{print $1}" | sed "s/://" | cut -d " " -f 1 | sort --unique').read().split('\n')
    return lines

def main():
    mainPrograms = getSoftwareWithGUI()
    lines = os.popen('dpkg -l | grep "^ii"').read().split('\n')
    i = 0
    while len([l for l in lines[i].split('  ') if l]) != 5:
        i += 1
    offsets = [lines[i].index(l) for l in lines[i].split('  ') if len(l)]
    pkgs = []
    for line in lines:
        parsed = []
        for i in range(len(offsets)):
            if len(offsets) == i + 1:
                parsed.append(line[offsets[i]:].strip())
            else:
                parsed.append(line[offsets[i]:offsets[i + 1]].strip())

        if len(parsed[1]) > 0:
            try:
                mainPrograms.index(parsed[1])
                parsed.append(True)
            except:
                parsed.append(False)
            pkgs.append({'Name':parsed[1], 'State':parsed[0], 'Version':parsed[2], 'Architecture':parsed[3], 'Description':parsed[4], 'HasGUI':parsed[5]})

    json_output = json.dumps(pkgs)

    # Print results to stdout
    print(json_output)
    sys.exit(0)

if __name__ == "__main__":
    main()