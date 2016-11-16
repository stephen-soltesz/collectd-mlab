# Debugging Disco Auto-discovery

Login to the `mlab_utility` slice at the site of your choice and setup some
convenience variables.

```
ssh mlab_utility@mlab1.{site}.measurement-lab.org
COMM=`cat /home/mlab_utility/conf/snmp.community.updated`
SWITCH="s1.${HOSTNAME#*.}"
```

## Running Disco config

The `disco_config.py` command line tool should generate the contents for
`/etc/collectd-snmp.conf`. Normally this is done every time `service collectd
start` or `service collectd restart`, but the error output may be hidden.

```
disco_config.py --command collectd-snmp-config \
    --community_file=/home/mlab_utility/conf/snmp.community \
	--hostname $SWITCH
```

## QFX and HP Proliant

Learn the switch model.
```
$ snmpget -v 2c -c $COMM $SWITCH sysDescr.0
SNMPv2-MIB::sysDescr.0 = STRING: Juniper Networks, Inc. qfx5100-48s-6q Ethernet Switch, kernel JUNOS 14.1X53-D35.3, Build date: 2016-02-29 23:39:06 UTC Copyright (c) 1996-2016 Juniper Networks, Inc.
```

Lookup the local machine MAC and uplink MAC addresses using `ifconfig` and
`arp`. For example:

```
$ ifconfig eth0 | grep HWaddr
eth0      Link encap:Ethernet  HWaddr F4:52:14:13:33:F0

$ arp
Address                  HWtype  HWaddress           Flags Mask            Iface
165.117.240.1            ether   00:12:c0:88:05:01   C                     eth0
```

Lookup the MAC addresses learned on each port using the
"Q-BRIDGE-MIB::dot1qTpFdbPort" OID. Be aware that MAC addresses are represented
in "dotted decimal" form in SNMP rather than the more common "colon
hexadecimal" form. The MAC is the last six digits of the returned OIDs. The
port number is the value on the right hand side.

```
$ snmpwalk -v 2c -c $COMM $SWITCH .1.3.6.1.2.1.17.7.1.2.2.1.2
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.0.18.192.136.5.1 = INTEGER: 1010
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.228.29.45.23.231.128 = INTEGER: 1083
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.244.82.20.19.51.16 = INTEGER: 1059
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.244.82.20.19.51.48 = INTEGER: 1035
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.244.82.20.19.51.240 = INTEGER: 1011
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.244.142.56.205.83.200 = INTEGER: 1084
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.244.142.56.205.84.68 = INTEGER: 1060
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.244.142.56.205.84.72 = INTEGER: 1036
SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.196608.244.142.56.205.84.80 = INTEGER: 1012
```

Lookup the ifIndex for the uplink and local ports using the port values above
for the corresponding MAC address. Append the port value to the end of the
"BRIDGE-MIB::dot1dBasePortIfIndex" OID.

```
$ snmpget -v 2c -c $COMM $SWITCH BRIDGE-MIB::dot1dBasePortIfIndex.1010
BRIDGE-MIB::dot1dBasePortIfIndex.1010 = INTEGER: 517

$ snmpget -v 2c -c $COMM $SWITCH BRIDGE-MIB::dot1dBasePortIfIndex.1011
BRIDGE-MIB::dot1dBasePortIfIndex.1011 = INTEGER: 512
```

If the lookup fails, you may get an error like:
```
$ snmpget -v 2c -c $COMM $SWITCH BRIDGE-MIB::dot1dBasePortIfIndex.1018
BRIDGE-MIB::dot1dBasePortIfIndex.1018 = No Such Instance currently exists at this OID
```

If the above fails, try walking all values at "BRIDGE-MIB::dot1dBasePortIfIndex".
Some ports may be missing.

```
$ snmpwalk -v 2c -c $COMM $SWITCH BRIDGE-MIB::dot1dBasePortIfIndex
BRIDGE-MIB::dot1dBasePortIfIndex.1010 = INTEGER: 517
BRIDGE-MIB::dot1dBasePortIfIndex.1011 = INTEGER: 512
BRIDGE-MIB::dot1dBasePortIfIndex.1012 = INTEGER: 519
BRIDGE-MIB::dot1dBasePortIfIndex.1035 = INTEGER: 513
BRIDGE-MIB::dot1dBasePortIfIndex.1036 = INTEGER: 520
BRIDGE-MIB::dot1dBasePortIfIndex.1059 = INTEGER: 515
BRIDGE-MIB::dot1dBasePortIfIndex.1060 = INTEGER: 521
BRIDGE-MIB::dot1dBasePortIfIndex.1083 = INTEGER: 516
BRIDGE-MIB::dot1dBasePortIfIndex.1084 = INTEGER: 523
```

The VLANs are configured according to "dot1qVlanStaticName"
```
$ snmpwalk -v 2c -c $COMM $SWITCH .1.3.6.1.2.1.17.7.1.4.3.1.1
```

## Cisco
