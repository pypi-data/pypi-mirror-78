import appoptics_apm.inst_logging as inst_logging
from appoptics_apm.util import *
from appoptics_apm.version import __version__
"""The AppOptics APM initializer will be executed when this package is imported by user application"""
config = AppOpticsApmConfig()
appoptics_apm_init()
# Report an status event after everything is done.
report_layer_init('Python')

inst_logging.wrap_logging_module()
get_log_trace_id = inst_logging.get_log_trace_id
