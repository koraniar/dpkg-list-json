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
    return os.popen('dpkg --search "*.desktop" | cut -d ":" -f 1 | sort --unique').read().split('\n')

def getSoftwareInstallationdate():
    lines = os.popen('grep " installed " /var/log/dpkg.log').read().split('\n')
    for i in range(len(lines)):
        information = lines[i].split(' ')
        if len(information) >= 4:
            lines[i] = [information[4].split(':')[0], information[0] + ' ' + information[1]]
        else:
            lines[i] = ['', '']
    return lines

def getInstallationDate(softwareName, installationDates):
    for installationDate in installationDates:
        if installationDate[0] == softwareName:
            return installationDate[1]
    return ''

def getPackageDetail(packageName, detailName):
    return os.popen('dpkg -s ' + packageName + ' | grep ' + detailName + ' | cut -d ":" -f 2').read().strip()

def parseSoftwareVendor(vendor, removeEmail):
    finalVendors = []
    if removeEmail:
        vendors = vendor.replace('\n', '').split('>')
        for vendorEmail in vendors:
            finalVendors.append(vendorEmail.split('<')[0])
        return '|'.join(finalVendors)[:-1]
    return vendor

def main():
    mainPrograms = getSoftwareWithGUI()
    installationDate = getSoftwareInstallationdate()
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
            parsed.append(getInstallationDate(parsed[1], installationDate))
            try:
                mainPrograms.index(parsed[1])
                parsed.append(True)
                parsed.append(parseSoftwareVendor(getPackageDetail(parsed[1], 'Maintainer'), True))
                parsed.append(getPackageDetail(parsed[1], 'Installed-Size'))
                pkgs.append({'Name':parsed[1], 'State':parsed[0], 'Version':parsed[2],
                'Architecture':parsed[3], 'Description':parsed[4], 'HasGUI':parsed[6],
                'Maintainer':parsed[7], 'Size':parsed[8], 'InstallationDate':parsed[5]})
            except:
                parsed.append(False)

    json_output = json.dumps(pkgs)

    # Print results to stdout
    print(json_output)
    sys.exit(0)

if __name__ == "__main__":
    main()