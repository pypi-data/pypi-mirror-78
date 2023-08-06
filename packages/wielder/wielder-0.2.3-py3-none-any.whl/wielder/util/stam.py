#!/usr/bin/env python
import logging

from wielder.util.log_util import setup_logging
from wielder.util.util import get_pod_actions, block_for_action
from wielder.wield.deployer import get_pods


if __name__ == "__main__":

    setup_logging(log_level=logging.DEBUG)
    slumber = 5
    _var_name = 'init_db'
    _var_value = 'done'

    _namespace = 'wielder-services'

    pods = get_pods('monitor', namespace=_namespace)

    _pod_name = pods[0].metadata.name

    block_for_action(_namespace, _pod_name, _var_name, _var_value)
    _var_name = 'init_topics'
    # block_for_action(_namespace, _pod_name, _var_name, _var_value)

