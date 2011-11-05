"""
Openstack run_tests.py style output for nosetests
"""

import logging

from nose import plugins

class Openstack(plugins.Plugin):
    """Nova style output generator"""

    name = "openstack"
