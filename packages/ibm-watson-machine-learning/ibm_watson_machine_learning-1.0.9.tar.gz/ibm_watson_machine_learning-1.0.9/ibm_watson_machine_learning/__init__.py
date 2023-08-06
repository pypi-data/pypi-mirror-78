"""Package skeleton

.. moduleauthor:: Wojciech Sobala <wojciech.sobala@pl.ibm.com>
"""

from os.path import join as path_join
import pkg_resources
import sys

try:
    wml_location = pkg_resources.get_distribution("ibm-watson-machine-learning").location
    sys.path.insert(1, path_join(wml_location, 'ibm_watson_machine_learning', 'libs'))
    sys.path.insert(2, path_join(wml_location, 'ibm_watson_machine_learning', 'tools'))
except pkg_resources.DistributionNotFound:
    pass
from ibm_watson_machine_learning.utils import version
from ibm_watson_machine_learning.client import APIClient

from .utils import is_python_2
if is_python_2():
    from ibm_watson_machine_learning.utils.log_util import get_logger
    logger = get_logger('wml_client_initialization')
    logger.warning("Python 2 is not officially supported.")
