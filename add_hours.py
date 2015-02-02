import models

import settings

import datetime

from sqlalchemy import and_

start_date = datetime.date(2015, 1, 26)

end_date = datetime.date(2015, 2, 2)

hours_dict = {}

total_hours = 0;

session = models.Session()

for log_id, task_name, start_time, end_time in session.query(models.WorkLog.id, models.Task.name, models.WorkLog.start_time, models.WorkLog.end_time).filter(and_(models.WorkLog.start_time > start_date, models.WorkLog.end_time < end_date)).join(models.Task, models.Task.id == models.WorkLog.task_id):
    
    if task_name not in hours_dict:
        hours_dict[task_name] = 0
    
    this_task_hours = (end_time - start_time).seconds / 3600.0
    hours_dict[task_name] += this_task_hours
    total_hours += this_task_hours
    
for task in hours_dict:
    print("{}: {:f} hours".format(task, hours_dict[task]))
    
print("Total hours: {:f}".format(total_hours))

