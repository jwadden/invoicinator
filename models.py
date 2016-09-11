import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

engine = None
Session = None

Base = sqlalchemy.ext.declarative.declarative_base()

def init_engine(settings_dict):
    global engine
    global Session
    engine = sqlalchemy.create_engine(settings_dict['db_engine'], echo=settings_dict['debug'])
    Session = sqlalchemy.orm.sessionmaker(bind=engine)

class Task(Base):
    __tablename__ = 'task'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Unicode(255))
    
    def __repr__(self):
        return "<Task(title='%s')>" % (self.name)
        
class WorkLog(Base):
    __tablename__ = 'work_log'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('task.id'))
    start_time = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
    end_time = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return "<WorkLog(task='%d', start='%s', end='%s')>" % (self.task_id, str(self.start_date), str(self.end_date))

