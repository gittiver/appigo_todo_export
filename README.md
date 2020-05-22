# appigo_todo_export
export task data from Appigo todo data

* database path: 
sqlite3 ~/Library/Containers/com.appigo.todomac/Data/Library/Application\ Support/Appigo\ Todo/AppigoTodo_v13.sqlitedb

* currently using query:
select name,type,type_data,recurrence,advanced_recurrence from tasks where deleted=0 and completion_date=-62135769600.0 order by parent_id

Currently all items are converted to TODO items with other columns as
properties

#TODO 
* read projects as toplevel todo, attach tasks as child TODO items
* read simpler task types and attach them to parent projct or list
* decode taskdata for tasktype 2
* decode dates
* decode recurrences
