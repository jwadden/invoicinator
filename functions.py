import models
import settings
import datetime

from sqlalchemy import and_

def get_hours(start_date, end_date):
    hours_dict = {}

    session = models.Session()

    for log_id, task_name, start_time, end_time in session.query(models.WorkLog.id, models.Task.name, models.WorkLog.start_time, models.WorkLog.end_time).filter(and_(models.WorkLog.start_time > start_date, models.WorkLog.end_time < end_date)).join(models.Task, models.Task.id == models.WorkLog.task_id):
        
        if task_name not in hours_dict:
            hours_dict[task_name] = 0
        
        this_task_hours = (end_time - start_time).seconds / 3600.0
        hours_dict[task_name] += this_task_hours

    return hours_dict
