import sqlalchemy
import sqlalchemy.ext.declarative
from optparse import OptionParser

import models
import settings

option_parser = OptionParser()
option_parser.add_option(
    "-s", "--settings",
    dest="settings",
    help="Settings",
    metavar="SETTINGS"
)

(options, args) = option_parser.parse_args()

try:
    settings_dict = settings.config[options.settings]
except:
    settings_dict = settings.config[settings.default_config]

models.init_engine(settings_dict)

models.Base.metadata.create_all(models.engine)
