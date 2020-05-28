# appigo_todo_export
export task data from Appigo todo data

* database path: 
sqlite3 ~/Library/Containers/com.appigo.todomac/Data/Library/Application\ Support/Appigo\ Todo/AppigoTodo_v13.sqlitedb

* currently using query:
select name,type,type_data,recurrence,advanced_recurrence from tasks where deleted=0 and completion_date=-62135769600.0 order by parent_id

Currently all items are converted to TODO items with other columns as
properties

#Structure of Tasks table
`
CREATE TABLE tasks(task_id TEXT PRIMARY KEY,
list_id TEXT,
name TEXT,
due_date DOUBLE,
completion_date DOUBLE,
priority INTEGER,
note TEXT,
mod_date DOUBLE,
deleted INTEGER,
dirty INTEGER,
sync_id TEXT,
local_sync_id TEXT,
start_date DOUBLE,
parent_sync_id TEXT,
recurrence INTEGER,
advanced_recurrence TEXT,
context_id TEXT,
tags TEXT,
flags INTEGER,
type INTEGER,
type_data TEXT,
parent_id TEXT,
sort_order INTEGER,
ds_due_date DOUBLE,
ds_priority INTEGER,
ps_due_date DOUBLE,
ps_priority INTEGER,
child_count INTEGER,
time_zone_offset INTEGER,
alert_dirty INTEGER,
starred INTEGER,
location_alert TEXT,
expansion_properties TEXT,
assigned_user_id TEXT,

project_due_date DOUBLE,
project_time_zone_offset INTEGER,
project_start_date DOUBLE,
project_priority INTEGER,
project_starred INTEGER,
start_date_time_zone_offset INTEGER,
project_start_date_time_zone_offset INTEGER);

`
#TODO 
* read projects as toplevel todo, attach tasks as child TODO items (DONE)
* read simpler task types and attach them to parent projct or list (DONE)
* decode taskdata for tasktype 2
* decode dates (DONE)
* decode recurrences (DONE)
