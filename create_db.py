import sqlalchemy
import sqlalchemy.ext.declarative

import models

models.Base.metadata.create_all(models.engine)
