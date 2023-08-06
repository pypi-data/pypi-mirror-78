# pyateos-ansible
Ansible module for [pyATEOS](https://github.com/lvrfrc87/pyATEOS) framework.

### Install:

To install just run the command:

`pip install pyateos-ansible`

### Configure Ansible:

Edit your `ansible.cfg` file and add the path where `eos_pyateos` module is installed.

i.e.

```
[defaults]
library = ./lib/python3.7/site-packages/pyateos-ansible/modules
```

If you run a `virtualenv` most probably the path would be something similar to the example above. 
Otherwise you can use for example `mlocate` to find where the module is.

For more info, have a look to [Ansible Docs](https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html#library)


### Module Documentation:

```
options:
    test:
        description:
            - One ore more test to be run. Every test correspond to a specific "show" command
            i.e. ntp - show ntp associations.
            For more details: https://gitlab.com/networkAutomation/pyateos/-/blob/master/README.md
        choices: [
            'acl',
            'arp',
            'as_path',
            'bgp_evpn',
            'bgp_ipv4',
            'interface',
            'ip_route',
            'mac',
            'mlag',
            'ntp',
            'lldp',
            'prefix_list',
            'route_map',
            'snmp',
            'stp',
            'vlan',
            'vrf',
            'vxlan',
            'bfd']
        type: list
    before:
        description:
            - Run pre-check tests defined under 'test' and generate .json.
            The fiename and directory path is the following: /tests/before/hostname/timestamp.json
        default: false
        type: bool
    after:
        description:
            - Run post-check tests defined under 'test'.
            The fiename and directory path is the following: /tests/after/hostname/timestamp.json
        default: false
        type: bool
    diff:
        description:
            - Run between vs. after diffs and save the result in .json format.
            The fiename and directory path is the following: /tests/diff/hostname/diff_timestamp_before_after.json
        default: false
        type: bool
    files:
        description:
            - List of before and after file IDs to compare in order to generate diff. Each file id
            is available under `result.before_file_ids` and `result.after_file_ids`
        type: list
    filter:
        description:
            - Valid only with `compare`. Filter reduces the output returning just the
            `insert` and `delete` in diff i.e. intrface - all interfaces counters are filtered.
        type: bool
        default: false
    group:
        description:
            - Pre set group of test. `group` and `test` are allowed togehter.
            For more details: https://gitlab.com/networkAutomation/pyateos/-/blob/master/README.md
        type: list
        choices: [
            'mgmt',
            'routing',
            'layer2',
            'ctr',
            'all'
        ]
    hostname:
        description:
            - Device hostname required for filesystem build
        type: str
        required: true
```

### Examples:

```
- name: run BEFORE tests.
  eos_pyateos:
      before: true
      test:
          - acl
      group: 
          - mgmt
          - layer2
      hostname: "{{ inventory_hostname }}"
  register: result

- name: save BEFORE file IDs.
  delegate_to: 127.0.0.1
  set_fact:
      before_ids: "{{ result.before_file_ids }}"

- name: change mgmt config on switch.
  eos_config:
      lines:
          - no ntp server vrf mgmt 10.75.33.5
          - ntp server vrf mgmt 216.239.35.4
          - no snmp-server host 10.1.22.1 vrf mgmt version 2c snmp_pass
          - snmp-server host 10.1.22.9 vrf mgmt version 2c snmp_pass

- name: shutdown interface.
  eos_config:
      lines:
          - shutdown
      parents: interface Ethernet50/1

- name: edit ACL.
  eos_config:
      lines:
          - no 10
          - 10 remark pyATEOS TEST
      parents: ip access-list standard SNMP

- name: run AFTER tests.
  eos_pyateos:
      after: true
      test:
          - acl
      group:
          - mgmt
          - layer2
      hostname: "{{ inventory_hostname }}"
  register: result

- name: save AFTER file IDs.
  delegate_to: 127.0.0.1
      set_fact:
          after_ids: "{{ result.after_file_ids }}"
 
- name: run DIFF result.
  eos_pyateos:
      compare: true
      group:
          - mgmt
          - layer2
      test:
          - acl
      hostname: "{{ inventory_hostname }}"
      filter: true
      files: 
          - "{{ before_ids }}"
          - "{{ after_ids }}"
```
