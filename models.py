import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

import settings

engine = sqlalchemy.create_engine(settings.db_engine, echo=settings.debug)
Session = sqlalchemy.orm.sessionmaker(bind=engine)

Base = sqlalchemy.ext.declarative.declarative_base()

class Case(Base):
    __tablename__ = 'case'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Unicode(255))
    
    def __repr__(self):
        return "<Case(title='%s')>" % (self.name)
        
class WorkLog(Base):
    __tablename__ = 'item'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    case_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('case.id'))
    start_date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return "<WorkLog(case='%d', start='%s', end='%s')>" % (self.case_id, str(self.start_date), str(self.end_date))

