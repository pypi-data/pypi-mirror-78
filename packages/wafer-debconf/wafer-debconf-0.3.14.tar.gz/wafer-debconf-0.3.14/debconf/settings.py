from wafer.settings import *

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'debconf.context_processors.expose_time_zone',
    'debconf.context_processors.expose_debconf_online',
)

DEBCONF_ONLINE = False
