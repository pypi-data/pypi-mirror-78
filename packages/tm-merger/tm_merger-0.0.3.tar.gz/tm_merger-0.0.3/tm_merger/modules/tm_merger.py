#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Federico Olivieri (lvrfrc87@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: tm_merger
version_added: "2.10"
author: "Federico Olivieri (@Federico87)"
short_description: Arista EOS config merger.
description:
    - Providing tenant and base different config file, this module is able to merge the two 
    config in one, mantaining confign indentation, line order as well as idempotency
notes:
    - Tested against EOS 4.22.5M
options:
    base:
        description:
            - Config file path where base config is located.
        type: path
        required: true
    tenant:
        description:
            - Config file path where tenant config is located.
        type: path
        required: true
    candidate:
        description:
            - Output file name and folder path.
        type: path
        required: true
requirements:
    - more_itertools
"""

EXAMPLES = """
---
- name: merge base.j2 with tenant.j2.
  tm_merger:
    base: ./configurations/{{ inventory_hostname }}/renders/{{ config_file_name }}.cfg
    tenant: ./configurations/{{ inventory_hostname }}/renders/tenants/{{ config_file_name }}.cfgfg
    file: ./configurations/{{ inventory_hostname }}/renders/candidate/{{ config_file_name }}.cfg
"""

RETURN = """
candidate:
  description: file candidate config
  returned: always
  type: list
"""
import os
import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib

try:
    import more_itertools as mit
    HAS_MORE_ITERTOOLS = True
except ImportError:
    HAS_MORE_ITERTOOLS = False


def vlans():

    global BASE_CONF

    vlans = list()
    vlan_map = dict()
    line_number = list()

    base_split = BASE_CONF.split('!')
    tenant_split = TENANT_CONF.split('!')

    # add new line in tenant vlans if not already
    if tenant_split[0][0] != '\n':
        tenant_split.insert(0, '\n' + tenant_split[0])

    # remove vlan anchor from base config
    for line in base_split:
        if '$VLAN$' in line:
            vlans.append(line.replace('$VLAN$',''))

    # remove vlan anchor from tenant config
    for line in tenant_split:
        if '$VLAN$' in line:
            vlans.append(line.replace('$VLAN$',''))

    # create vlan dict() with vlan id as key for later sorting
    for vlan_id in vlans:
        vlan_map[int(vlan_id.rstrip().replace('vlan','').split()[0])] = vlan_id

    base_splitlines = BASE_CONF.splitlines()

    # find vlan line number in base config
    for number,line in enumerate(base_splitlines):
        if '$VLAN$' in line:
            line_number.append(number)

    # delete vlan lines from base config
    del base_splitlines[line_number[0]:line_number[-1] ]

    # insert sorted vlan lines in base config
    for key in reversed(sorted(vlan_map)):
        base_splitlines.insert(line_number[0], vlan_map[key].replace('\nvlan', '!\nvlan').rstrip())
    
    # remove double "!" at beginning of vlan config lines 
    if base_splitlines[line_number[0]].startswith('!\n'):
       base_splitlines[line_number[0]] = base_splitlines[line_number[0]].replace('!\n', '', 1)

    # edit last line $VLAN$!
    for number,line in enumerate(base_splitlines):
        if line.startswith('$VLAN$'):
            base_splitlines[number] = base_splitlines[number].replace(line, '!', 1)

    BASE_CONF = '\n'.join(base_splitlines)


def vrf():

    global BASE_CONF

    vrfs = list()
    line_number = list()

    base_split = BASE_CONF.split('!')
    tenant_split = TENANT_CONF.split('!')

    # remove vrf anchor from base config
    for line in base_split:
        if '$VRF$' in line:
            vrfs.append(line.replace('$VRF$',''))

    # remove vrf anchor from tenant config
    for line in tenant_split    :
        if '$VRF$' in line:
            vrfs.append(line.replace('$VRF$',''))

    base_splitlines = BASE_CONF.splitlines()

    # find vrf line number in base config
    for number,line in enumerate(base_splitlines):
        if '$VRF$' in line:
            line_number.append(number)

    # delete vrf lines from base config
    del base_splitlines[line_number[0]:line_number[-1] ]

    # insert sorted vrf lines in base config
    for vrf in reversed(sorted(vrfs)):
        base_splitlines.insert(line_number[0], vrf.replace('\nvrf', '!\nvrf').rstrip())

    # remove double "!" at beginning of vrf config lines 
    if base_splitlines[line_number[0]].startswith('!\n'):
       base_splitlines[line_number[0]] = base_splitlines[line_number[0]].replace('!\n', '', 1)
 
    # replace last line "$VRF$!" with "!"
    for number,line in enumerate(base_splitlines):
        if line.startswith('$VRF$'):
            base_splitlines[number] = base_splitlines[number].replace(line, '!', 1)
    
    BASE_CONF = '\n'.join(base_splitlines)


def port_channel():

    global BASE_CONF

    tenant_vlan_id = list()
    po_vlan_line = int()

    candidate = BASE_CONF.splitlines()

    # find tenant vlan IDs
    for line in TENANT_CONF.split():
        if '$PO$' in line:
            if '$PO$!' not in line:
                tenant_vlan_id.append(int(line.strip('$PO$')))

    # find vlans line in PortChannel7 configuration
    for number,line in enumerate(candidate):
        if 'interface Port-Channel7' in line:
            index_line = number
            while True:
                if 'switchport trunk allowed vlan' not in candidate[index_line]:
                    index_line = index_line + 1
                else:
                    po_vlan_line = index_line
                    break

    # find vlans in PO config -> str() 99,101-103,999
    candidate_vlan = candidate[po_vlan_line].split()[4]

    # split string and find vlan range  -> list()
    for i in candidate_vlan.split(','):
        # str() '101-103'
        if '-' in i:
            # find each vlan in range
            for k in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1 ):
                tenant_vlan_id.append(int(k))
        else:
          tenant_vlan_id.append(int(i))

    tenant_vlan_id.sort()

    # create list fir each vlan or range [[99], [101, 102, 103], [141], [666], [999]]
    super_list = [list(group) for group in mit.consecutive_groups(tenant_vlan_id)]

    # find consecutive VLAN IDs [101, 102, 103]
    for number,line in enumerate(super_list):
        if len(line) > 1:
            super_list.pop(number)
            super_list.insert(number, [str(line[0]) + '-' + str(line[-1])])
            # remove nested lists -> list() [99, '101-103', 141, 666, 999]
            flatten = [item for sublist in super_list for item in sublist]
        else:
            flatten = list()
            for i in super_list:
                flatten.append(i[0])

    # join vlan elements -> str() 99,101-103,141,666,999
    vlan_ids = ','.join(str(e) for e in flatten)
    candidate[index_line] = '   switchport trunk allowed vlan {}'.format(vlan_ids)

    BASE_CONF = '\n'.join(candidate)


def eth30():

    global BASE_CONF

    tenant_vlan_id = list()
    po_vlan_line = int()

    candidate = BASE_CONF.splitlines()

    # find tenant vlan IDs
    for line in TENANT_CONF.split():
        if '$PO$' in line:
            if '$PO$!' not in line:
                tenant_vlan_id.append(int(line.strip('$PO$')))

    # find vlans line in PortChannel7 configuration
    for number,line in enumerate(candidate):
        if 'interface Ethernet30' in line:
            index_line = number
            while True:
                if 'switchport trunk allowed vlan' not in candidate[index_line]:
                    index_line = index_line + 1
                else:
                    po_vlan_line = index_line
                    break

    # find vlans in PO config -> str() 99,101-103,999
    candidate_vlan = candidate[po_vlan_line].split()[4]

    # split string and find vlan range  -> list()
    for i in candidate_vlan.split(','):
        # str() '101-103'
        if '-' in i:
            # find each vlan in range
            for k in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1 ):
                tenant_vlan_id.append(int(k))
        else:
          tenant_vlan_id.append(int(i))

    tenant_vlan_id.sort()

    # create list fir each vlan or range [[99], [101, 102, 103], [141], [666], [999]]
    super_list = [list(group) for group in mit.consecutive_groups(tenant_vlan_id)]

    # find consecutive VLAN IDs [101, 102, 103]
    for number,line in enumerate(super_list):
        if len(line) > 1:
            super_list.pop(number)
            super_list.insert(number, [str(line[0]) + '-' + str(line[-1])])
            # remove nested lists -> list() [99, '101-103', 141, 666, 999]
            flatten = [item for sublist in super_list for item in sublist]
        else:
            flatten = list()
            for i in super_list:
                flatten.append(i[0])

    # join vlan elements -> str() 99,101-103,141,666,999
    vlan_ids = ','.join(str(e) for e in flatten)
    candidate[index_line] = '   switchport trunk allowed vlan {}'.format(vlan_ids)

    BASE_CONF = '\n'.join(candidate)


def eth31():

    global BASE_CONF

    tenant_vlan_id = list()
    po_vlan_line = int()

    candidate = BASE_CONF.splitlines()

    # find tenant vlan IDs
    for line in TENANT_CONF.split():
        if '$PO$' in line:
            if '$PO$!' not in line:
                tenant_vlan_id.append(int(line.strip('$PO$')))

    # find vlans line in PortChannel7 configuration
    for number,line in enumerate(candidate):
        if 'interface Ethernet31' in line:
            index_line = number
            while True:
                if 'switchport trunk allowed vlan' not in candidate[index_line]:
                    index_line = index_line + 1
                else:
                    po_vlan_line = index_line
                    break

    # find vlans in PO config -> str() 99,101-103,999
    candidate_vlan = candidate[po_vlan_line].split()[4]

    # split string and find vlan range  -> list()
    for i in candidate_vlan.split(','):
        # str() '101-103'
        if '-' in i:
            # find each vlan in range
            for k in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1 ):
                tenant_vlan_id.append(int(k))
        else:
          tenant_vlan_id.append(int(i))

    tenant_vlan_id.sort()

    # create list fir each vlan or range [[99], [101, 102, 103], [141], [666], [999]]
    super_list = [list(group) for group in mit.consecutive_groups(tenant_vlan_id)]

    # find consecutive VLAN IDs [101, 102, 103]
    for number,line in enumerate(super_list):
        if len(line) > 1:
            super_list.pop(number)
            super_list.insert(number, [str(line[0]) + '-' + str(line[-1])])
            # remove nested lists -> list() [99, '101-103', 141, 666, 999]
            flatten = [item for sublist in super_list for item in sublist]
        else:
            flatten = list()
            for i in super_list:
                flatten.append(i[0])

    # join vlan elements -> str() 99,101-103,141,666,999
    vlan_ids = ','.join(str(e) for e in flatten)
    candidate[index_line] = '   switchport trunk allowed vlan {}'.format(vlan_ids)

    BASE_CONF = '\n'.join(candidate)


def eth32():

    global BASE_CONF

    tenant_vlan_id = list()
    po_vlan_line = int()

    candidate = BASE_CONF.splitlines()

    # find tenant vlan IDs
    for line in TENANT_CONF.split():
        if '$PO$' in line:
            if '$PO$!' not in line:
                tenant_vlan_id.append(int(line.strip('$PO$')))

    # find vlans line in PortChannel7 configuration
    for number,line in enumerate(candidate):
        if 'interface Ethernet32' in line:
            index_line = number
            while True:
                if 'switchport trunk allowed vlan' not in candidate[index_line]:
                    index_line = index_line + 1
                else:
                    po_vlan_line = index_line
                    break

    # find vlans in PO config -> str() 99,101-103,999
    candidate_vlan = candidate[po_vlan_line].split()[4]

    # split string and find vlan range  -> list()
    for i in candidate_vlan.split(','):
        # str() '101-103'
        if '-' in i:
            # find each vlan in range
            for k in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1 ):
                tenant_vlan_id.append(int(k))
        else:
          tenant_vlan_id.append(int(i))

    tenant_vlan_id.sort()

    # create list fir each vlan or range [[99], [101, 102, 103], [141], [666], [999]]
    super_list = [list(group) for group in mit.consecutive_groups(tenant_vlan_id)]

    # find consecutive VLAN IDs [101, 102, 103]
    for number,line in enumerate(super_list):
        if len(line) > 1:
            super_list.pop(number)
            super_list.insert(number, [str(line[0]) + '-' + str(line[-1])])
            # remove nested lists -> list() [99, '101-103', 141, 666, 999]
            flatten = [item for sublist in super_list for item in sublist]
        else:
            flatten = list()
            for i in super_list:
                flatten.append(i[0])

    # join vlan elements -> str() 99,101-103,141,666,999
    vlan_ids = ','.join(str(e) for e in flatten)
    candidate[index_line] = '   switchport trunk allowed vlan {}'.format(vlan_ids)

    BASE_CONF = '\n'.join(candidate)


def eth33():

    global BASE_CONF

    tenant_vlan_id = list()
    po_vlan_line = int()

    candidate = BASE_CONF.splitlines()

    # find tenant vlan IDs
    for line in TENANT_CONF.split():
        if '$PO$' in line:
            if '$PO$!' not in line:
                tenant_vlan_id.append(int(line.strip('$PO$')))

    # find vlans line in PortChannel7 configuration
    for number,line in enumerate(candidate):
        if 'interface Ethernet33' in line:
            index_line = number
            while True:
                if 'switchport trunk allowed vlan' not in candidate[index_line]:
                    index_line = index_line + 1
                else:
                    po_vlan_line = index_line
                    break

    # find vlans in PO config -> str() 99,101-103,999
    candidate_vlan = candidate[po_vlan_line].split()[4]

    # split string and find vlan range  -> list()
    for i in candidate_vlan.split(','):
        # str() '101-103'
        if '-' in i:
            # find each vlan in range
            for k in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1 ):
                tenant_vlan_id.append(int(k))
        else:
          tenant_vlan_id.append(int(i))

    tenant_vlan_id.sort()

    # create list fir each vlan or range [[99], [101, 102, 103], [141], [666], [999]]
    super_list = [list(group) for group in mit.consecutive_groups(tenant_vlan_id)]

    # find consecutive VLAN IDs [101, 102, 103]
    for number,line in enumerate(super_list):
        if len(line) > 1:
            super_list.pop(number)
            super_list.insert(number, [str(line[0]) + '-' + str(line[-1])])
            # remove nested lists -> list() [99, '101-103', 141, 666, 999]
            flatten = [item for sublist in super_list for item in sublist]
        else:
            flatten = list()
            for i in super_list:
                flatten.append(i[0])

    # join vlan elements -> str() 99,101-103,141,666,999
    vlan_ids = ','.join(str(e) for e in flatten)
    candidate[index_line] = '   switchport trunk allowed vlan {}'.format(vlan_ids)

    BASE_CONF = '\n'.join(candidate)


def iface():

    global BASE_CONF

    svi = list()
    svi_map = dict()
    line_number = list()

    base_split = BASE_CONF.split('!')
    tenant_split = TENANT_CONF.split('!')
    
    for line in tenant_split:
        if '$IFACE$' in line:
            svi.append(line.replace('$IFACE$',''))

    for line in base_split:
        if '$IFACE$' in line:
            svi.append(line.replace('$IFACE$',''))

    for svi_id in svi:
        svi_match = re.search(r'(interface\sVlan)(\d+)', svi_id)
        if svi_match:
            svi_map[int(svi_match.group(2))] = svi_id

    base_splitlines = BASE_CONF.splitlines()

    for number,line in enumerate(base_splitlines):
        if '$IFACE$' in line:
            line_number.append(number)

    del base_splitlines[line_number[0]:line_number[-1]]

    for key in reversed(sorted(svi_map)):
        base_splitlines.insert(line_number[0], svi_map[key].replace('\ninterface', '!\ninterface').rstrip())

    if base_splitlines[line_number[0]].startswith('!\n'):
       base_splitlines[line_number[0]] = base_splitlines[line_number[0]].replace('!\n', '', 1)

    for number,line in enumerate(base_splitlines):
        if line.startswith('$IFACE$'):
            base_splitlines[number] = base_splitlines[number].replace(line, '!', 1)

    BASE_CONF = '\n'.join(base_splitlines)


def vxlan():

    global BASE_CONF

    vxlan = list()
    vxlan_vlan_map = dict()
    vxlan_vrf_map = dict()
    line_number_vlan = list()
    line_number_vrf = list()
    vxlan_ids = list()

    tenant_split = TENANT_CONF.split('!')
    base_splitlines = BASE_CONF.splitlines()

    for line in tenant_split:
        if '$VXLAN$' in line:
            vxlan_ids.append(line.replace('$VXLAN$','').strip())

    for number,line in enumerate(base_splitlines):
        if '$VXLAN$' in line:
            if 'vlan' in line:
                vxlan.append(line.replace('$VXLAN$',''))
                line_number_vlan.append(number)

    for vlan in vxlan:
        vxlan_vlan_match = re.search(r'(vxlan\svlan\s)(\d+)', vlan)

        if vxlan_vlan_match:
            vxlan_vlan_map[int(vxlan_vlan_match.group(2))] = vlan

    # build tenant vlan and vrf vxlan lines
    for vxlan_id in vxlan_ids:
        vxlan_vlan_map[int(vxlan_id)] = '   vxlan vlan {0} vni {0}'.format(vxlan_id)
        vxlan_vrf_map[str('t' + vxlan_id)] = '   vxlan vrf t{0} vni 1{0}'.format(vxlan_id)

    del base_splitlines[line_number_vlan[0]:line_number_vlan[-1] + 1]

    # insert vxlan vlan in candidate
    for key in reversed(sorted(vxlan_vlan_map)):
        base_splitlines.insert(line_number_vlan[0], vxlan_vlan_map[key]) 

    # build vrf part of vxlan
    for number,line in enumerate(base_splitlines):
        if '$VXLAN$' in line:
            if 'vrf' in line:
                vxlan.append(line.replace('$VXLAN$',''))
                line_number_vrf.append(number)

    for vrf in vxlan:
        vxlan_vrf_match = re.search(r'(vxlan\svrf\s)(\S*)', vrf)

        if vxlan_vrf_match:
            vxlan_vrf_map[(vxlan_vrf_match.group(2))] = vrf

    del base_splitlines[line_number_vrf[0]:line_number_vrf[-1] + 1]

    # insert vxlan vrf in candidate
    for key in reversed(sorted(vxlan_vrf_map)):
        base_splitlines.insert(line_number_vrf[0], vxlan_vrf_map[key])

    for number,line in enumerate(base_splitlines):
        if line.startswith('$VXLAN$'):
            base_splitlines[number] = base_splitlines[number].replace(line, '!', 1)

    BASE_CONF = '\n'.join(base_splitlines)


def ip_route():

    global BASE_CONF

    route = list()
    line_number = list()

    base_splitlines = BASE_CONF.splitlines()
    tenant_splitlines = TENANT_CONF.splitlines()

    for line in tenant_splitlines:
        if '$ROUTE$' in line:
            route.append(line.replace('$ROUTE$','').strip())

    for number,line in enumerate(base_splitlines):
        if '$ROUTE$' in line:
            route.append(line.replace('$ROUTE$',''))
            line_number.append(number)
    
    del base_splitlines[line_number[0]:line_number[-1] + 1]

    for route in reversed(sorted(route)):
        if route != '!':
            base_splitlines.insert(line_number[0], route)

    BASE_CONF = '\n'.join(base_splitlines)


def routing():

    global BASE_CONF

    routing = list()
    line_number = list()

    base_splitlines = BASE_CONF.splitlines()
    tenant_splitlines = TENANT_CONF.splitlines()

    for i in tenant_splitlines:
        if '$ROUTING$' in i:
            routing.append(i.replace('$ROUTING$','').strip())

    for number,line in enumerate(base_splitlines):
        if '$ROUTING$' in line:
            routing.append(line.replace('$ROUTING$',''))
            line_number.append(number)
    
    del base_splitlines[line_number[0]:line_number[-1] + 1]

    for i in reversed(sorted(routing)):
        if i != '!':
            base_splitlines.insert(line_number[0], i)

    BASE_CONF = '\n'.join(base_splitlines)


def prefix():

    global BASE_CONF

    prefix = list()
    line_number = list()
    prefix_map = dict()
    tenant_line = list()

    base_splitlines = BASE_CONF.splitlines()
    tenant_splitlines = TENANT_CONF.splitlines()

    for number,line in enumerate(base_splitlines):
        if '$PREFIX$' in line:
            prefix.append(line.replace('$PREFIX$',''))
            line_number.append(number)
    
    for seq in prefix:
        prefix_map[int(seq.split()[4])] = seq
    
    for line in tenant_splitlines:
        if '$PREFIX$' in line:
            tenant_line.append(line.replace('$PREFIX$','').strip())


    count = int(prefix[-1].split()[4])
    for line in tenant_line:
        if line != '!': 
            count = count + 10
            line = line[0:32] + ' {} '.format(count) + line[33:]    
            prefix_map[int(count)] = line
            
    del base_splitlines[line_number[0]:line_number[-1] + 1]

    for key in reversed(sorted(prefix_map)):
        base_splitlines.insert(line_number[0], prefix_map[key])

    BASE_CONF = '\n'.join(base_splitlines)


def bgp():

    global BASE_CONF

    bgp_vlan = list()
    bgp_vrf = list()
    line_number_vlan = list()
    line_number_vrf = list()
    bgp_vrf_map = dict()

    tenant_split = TENANT_CONF.split('!')
    base_split = BASE_CONF.split('!')

    for line in tenant_split:
        if '$BGPVLAN$' in line:
            bgp_vlan.append(line.replace('$BGPVLAN$','').strip())

    for line in base_split:
        if '$BGPVLAN$' in line:
            bgp_vlan.append(line.replace('$BGPVLAN$','').strip())
    
    base_splitlines = BASE_CONF.splitlines()

    for number,line in enumerate(base_splitlines):
        if '$BGPVLAN$' in line:
            line_number_vlan.append(number)

    del base_splitlines[line_number_vlan[0]:line_number_vlan[-1] +1]
    
    for number,line in enumerate(reversed(sorted(bgp_vlan))):
        new_line = '   ' + line + '\n!'
        base_splitlines.insert(line_number_vlan[0], new_line)

    # build vrf part of bgp
    for line in tenant_split:
        if '$BGPVRF$' in line:
            bgp_vrf.append(line.replace('$BGPVRF$','').strip())
    
    for line in base_split:
        if '$BGPVRF$' in line:
            bgp_vrf.append(line.replace('$BGPVRF$',''))

    for number,line in enumerate(base_splitlines):
        if '$BGPVRF$' in line:
            line_number_vrf.append(number)

    del base_splitlines[line_number_vrf[0]:line_number_vrf[-1] + 1]

    for number, line in enumerate(bgp_vrf):

        if 'address-family ipv4' in line:
            line = bgp_vrf[number - 1 ] + '!' + line

        bgp_vrf_match = re.search(r'(vrf\s)(.*)', line)
        
        if bgp_vrf_match:
            bgp_vrf_map[bgp_vrf_match.group(2)] = line

    for key in reversed(sorted(bgp_vrf_map)):
        if  bgp_vrf_map[key].endswith('/n'):
            value = '   ' + bgp_vrf_map[key].lstrip() + '!'
        else:
            value = '   ' + bgp_vrf_map[key].lstrip() + '\n!'
        base_splitlines.insert(line_number_vrf[0], (value))
    
    BASE_CONF = '\n'.join(base_splitlines)


if __name__ == "__main__":
    argument_spec = dict(
            base=dict(required=True),
            tenant=dict(required=True),
            candidate=dict(required=True),
            hostname=dict(required=True),
        )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    if not HAS_MORE_ITERTOOLS:
        module.fail_json(msg=missing_required_lib("more_itertools"))

    try:
        BASE_CONF = open(module.params.get("base"), 'rt').read()
    except FileNotFoundError as error:
        module.fail_json(msg=error)

    try:
        TENANT_CONF = open(module.params.get("tenant"), 'rt').read()
    except FileNotFoundError as error:
        module.fail_json(msg=error)

    hostname = module.params.get("hostname")
    result = dict()
    result = {'changed': False}

    if '$VLAN$' in TENANT_CONF:
        vlans()
    if '$VRF$' in TENANT_CONF:
        vrf()
    if hostname == 'svc1a.r3b15.ams7.nee.tmcs':
        port_channel()
        eth30()
        eth31()
        eth32()
        eth33()
    elif hostname == 'svc2a.r4b15.ams7.nee.tmcs':
        port_channel()
        eth30()
        eth31()
        eth32()
        eth33()
    if '$IFACE$' in TENANT_CONF:
        iface()
    if '$VXLAN$' in TENANT_CONF:
        vxlan()
    if '$ROUTE$' in TENANT_CONF:
        ip_route()
    if '$ROUTING$' in TENANT_CONF:
        routing()
    if '$PREFIX$' in TENANT_CONF:
        prefix()
    if '$BGPVLAN$' in TENANT_CONF and '$BGPVRF$' in TENANT_CONF:
        bgp()


    try:
        with open(module.params.get("candidate"), "w") as candidate:
            candidate.write(BASE_CONF)    
    except:
        module.fail_json(msg="Something went wrong when writing to file")

    result["candidate"] = BASE_CONF
    
    if result:
        module.exit_json(**result)
