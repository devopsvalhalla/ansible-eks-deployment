
DOCUMENTATION = r'''
---
module: eks_deploy
short_description: Deploy EKS Cluster
version_added: "0.1.0"
author:
  - Trey Phillips (trey.phillips@devopsvalhalla.com)
requirements:
  - "terraform (https://github.com/)"
description:
  -  Deploys EKS cluster on AWS using Terraform
options:
  cluster_name:
    description:
      - Name of EKS cluster
    required: true
    type: string
  vpc_id:
    description:
      - ID of destination VPC
    required: true
    type: bool
  state:
    description:
      - Deploy or remove cluster
    required: true
    type: bool
  private:
    description:
      - Does this cluster use private endpoints?
    default: false
    type: bool
  cluster_network:
    description:
      - CIDR of internal cluster network
    required: true
    type: string
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''

import re
from posixpath import split
from typing_extensions import Required
from ansible.module_utils.basic import AnsibleModule


def validateCIDR(cluster_network):
    cidrFormat = re.search("\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b/[0-9]+", cluster_network)

    if not cidrFormat:
        module.fail_json(msg='The provided CIDR is not correctly formatted.')

    networkSize = split('/', cluster_network)[1]

    if networkSize < 12:
        module.fail_json(msg='Provided CIDR is too large, maximum size is /12')

    if networkSize > 24:
        module.fail_json(msg='Provided CIDR is too small, minimum size is /24')

    return None


def validateClusterName(cluster_name):
    nameValid = re.search("^[0-9A-Za-z][A-Za-z0-9\-_]+$", cluster_name)

    if not nameValid:
        module.fail_json(msg='EKS Cluster name does not meet AWS formatting ([0-9A-Za-z][A-Za-z0-9\-_]).')

    return None

def validateVersion(version):
    versValid = re.search("^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$", version)

    if not versValid:
        module.fail_json(msg='Provided Kubernetes version does not match semantic versioning format.')

    return None


def main():
    global module

    module = AnsibleModule(
        argument_spec=dict(
            cluster_name=dict(type='str', required=True),
            vpc_id=dict(type='string', required=True),
            cluster_network=dict(type='string'),
            cloudwatch_log=dict(type='bool', default=True),
            private=dict(type='bool', default=False),
            version=dict(type='string'),
            state=dict(
                choices=["present", "absent"], default="present", required=True
            )
        ),
        supports_check_mode=False,
    )

    validateClusterName()
    validateCIDR()
    validateVersion()


if __name__ == '__main__':
    main()