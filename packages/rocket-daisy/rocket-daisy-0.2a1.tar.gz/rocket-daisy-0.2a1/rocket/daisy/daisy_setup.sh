#!/bin/sh
#     ____        _
#    / __ \____ _(_)______  __
#   / / / / __ `/ / ___/ / / /
#  / /_/ / /_/ / (__  ) /_/ /
# /_____/\__,_/_/____/\__, /
# martin shishkov    /____/
#
#   Copyright 2020 Martin Shishkov, gulliversoft.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# Daisy setup script
SEARCH="python3"
FOUND=""
INSTALLED=""
if [ "$#" = "1" ]; then
        command="$1"
else
        command="none"
fi

echo
echo "Installing Daisy..."
echo

if [ "$command" != "skip-apt" ]; then
        echo "Updating apt package list..."
        apt-get update
        echo
fi

# Look up for installed python
for python in $SEARCH; do program="/usr/bin/$python"
        if [ -x $program ]; then
                FOUND="$FOUND $python"
                version=`$python -V 2>&1`
                include=`$python -c "import distutils.sysconfig; print(distutils.sysconfig.get_python_inc())"`
                echo "Found $version... "

                if [ "$command" != "skip-apt" ]; then
                        # Install required dev header and setuptools
                        echo "Trying to install $python-dev using apt-get"
                        apt-get install -y $python-dev $python-setuptools
                fi

                # Try to compile and install for the current python
                if [ -f "$include/Python.h" ]; then
                        echo "Trying to install Daisy for $version"
                        # $python setup.py install
                        # if [ "$?" -ne "0" ]; then
                                # Sub setup error, continue with next python
                        #        echo "Build for $version failed\n"
                        #        continue
                        # fi
                        echo "Daisy installed for $version \n"
                        INSTALLED="$INSTALLED $python"
                else
                        echo "Cannot install for $version : missing development headers\n"
                fi
        fi
done

# Ensure Daisy is installed to continue
if [ -z "$INSTALLED" ]; then
        if [ -z "$FOUND" ]; then
                echo "ERROR: Daisy cannot be installed - python3 not found"
                exit 1
        else
                echo "ERROR: Daisy cannot be installed - please check errors above"
                exit 2
        fi
fi

# Select greater python version
for python in $INSTALLED; do echo $python > /dev/null
done

# Update HTML resources
echo "Copying HTML resources..."
mkdir /usr/share/daisy 2>/dev/null 1>/dev/null
cp -rfv htdocs /usr/share/daisy
echo

# Add config file if it does not exist
if [ ! -f "/etc/daisy/config" ]; then
        echo "Copying default config file..."
        mkdir /etc/daisy 2>/dev/null 1>/dev/null
        cp -v config /etc/daisy/config
fi

# Add passwd file if it does not exist
if [ ! -f "/etc/daisy/passwd" ]; then
        echo "Copying default passwd file..."
        mkdir /etc/daisy 2>/dev/null 1>/dev/null
        cp -v passwd /etc/daisy/passwd
fi

# Add daisy-passwd command
echo "Installing daisy-passwd command..."
cp -rf daisy-passwd.py /usr/bin/daisy-passwd
sed -i "s/python/$python/g" /usr/bin/daisy-passwd
chmod 0755 /usr/bin/daisy-passwd

# Display Daisy usages
echo
echo "Daisy successfully installed"
echo "* To start Daisy foreground\t: sudo daisy [-h] [-c config] [-l log] [-s script] [-d] [port]"
echo
echo "     ____        _           "
echo "    / __ \____ _(_)______  __"
echo "   / / / / __  / / ___/ / / /"
echo "  / /_/ / /_/ / (__  ) /_/ / "
echo " /_____/\__,_/_/____/\__, /  "
echo " martin shishkov    /____/   "
echo

