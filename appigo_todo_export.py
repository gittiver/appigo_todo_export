#!/usr/bin/python
import sys
from os import path
import sqlite3
import datetime

tasktype = {
    0:"task",
    1: "project",
    2: "contact",
    6: "url"
}

recurrence_string = {
    0: "",
    1: "+1w",
    2: "+1m",
    3: "+1y",
    5: "+2w",
    7: "+6m",
    9: "",
    50: "+1m",
    101:"+1w",
    105: "+2w",
    150: "+3d",
    103: "+1y",
}
def convert_tasks(dbname):
        """
        opens database file with name dbname
        loads values from database and writes as org-mode formatted text to stdout
        """
     
        connection = sqlite3.connect(dbname)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("select name,type,type_data,recurrence,advanced_recurrence, task_id, parent_id, due_date, project_due_date, note from tasks where deleted=0 and completion_date=-62135769600.0 order by parent_id") 
        result = cursor.fetchall() 

        children = {}
        no_parent = []
        for r in result:
            if r['parent_id'] is None:
                no_parent.append(r)
            elif r['parent_id'] ==u'':
                no_parent.append(r)
            else:
                if r['parent_id'] in children:
                    children[r['parent_id']].append(r)
                else:
                    children[r['parent_id']] =[r]
                    
        level=1               
        for task in no_parent:
            convert_task(task,level)
            if task['task_id'] in children:
                for sub_task in children[task['task_id']]:
                    convert_task(sub_task,level+1)
                
        connection.close()

def deadline(date,recurrence,advanced_recurrence):
    if recurrence==0:
        return "<"+date+ ">"
        
    else:
        return "<"+ date +" " + recurrence_string[recurrence]+ ">"

def double_to_date(d):
    if d is None:
        return ""
    else:
        return datetime.datetime.fromtimestamp(d).strftime("%Y-%m-%d %a %H:%M")

def convert_task(row,level):
      """converts a single task row"""
      
      print level*'*',"TODO", row['name'].encode('utf-8')

      #convert due_date to DEADLINE entry
      if row['type']==1:
          # for project use project_due_date
          due_date = row['project_due_date']
      else:
          # for other than project use due_date
          due_date = row['due_date']
        
      if due_date < 64092211200.0:
            print "DEADLINE:", \
                      deadline(double_to_date(due_date),
                               row['recurrence'],
                               row['advanced_recurrence'])

      print ":PROPERTIES:"
      print ":Tasktype:",tasktype[row['type']]
      print ":type_data:", row['type_data'].encode('utf-8')
      print ":recurrence:", row['recurrence']
      print ":advanced_recurrence:", row['advanced_recurrence']
      print ":task_id:", row['task_id']
      print ":parent_id:", row['parent_id']
      print ":due_date:", row['due_date']
      print ":END:"
        
      if row['note'] !='':
            print row['note'].encode('utf8')
        
def main(argv):
    if len(argv)<1:
        inputfile = path.expanduser('~/Library/Containers/com.appigo.todomac/Data/Library/Application Support/Appigo Todo/AppigoTodo_v13.sqlitedb')
        
    else:
        inputfile = argv[0]

    print "#                  -*- mode: org -*-"
    print "#+TITLE: Import from Appigo Todo"
    print "#+OPTIONS: ^:{}"
    print ""

    convert_tasks(inputfile)
    
if __name__ == "__main__":
   main(sys.argv[1:])
