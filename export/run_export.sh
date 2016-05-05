#!/bin/bash

if test -s /home/mlab_utility/conf/snmp.community ; then
    /usr/bin/mlab_export.py --noupdate --suffix=switch --compress > /dev/null
fi
/usr/bin/mlab_export.py --compress > /dev/null
