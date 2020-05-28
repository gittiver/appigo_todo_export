#!/usr/bin/python
import sys
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
        cursor = connection.cursor()
        cursor.execute("select name,type,type_data,recurrence,advanced_recurrence, task_id, parent_id, due_date, project_due_date, note from tasks where deleted=0 and completion_date=-62135769600.0 order by parent_id") 
        result = cursor.fetchall() 

        children = {}
        no_parent = []
        for r in result:
            if r[6] is None:
                no_parent.append(r)
            elif r[6] ==u'':
                no_parent.append(r)
            else:
                if r[6] in children:
                    children[r[6]].append(r)
                else:
                    children[r[6]] =[r]
                    
        level=1               
        for task in no_parent:
            convert_task(task,level)
            if task[5] in children:
                for sub_task in children[task[5]]:
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
  #      print row
        print level*'*',"TODO", row[0].encode('utf-8')
        if row[1]==1:
                if row[8]<64092211200.0:
                        print "DEADLINE:", \
                          deadline(double_to_date(row[8]),row[3],row[4])
                
        elif row[7]<64092211200.0:
                print "DEADLINE:", \
                  deadline(double_to_date(row[7]),row[3],row[4])
        print ":PROPERTIES:"
        print ":Tasktype:",tasktype[row[1]]
        print ":type_data:", row[2].encode('utf-8')
        print ":recurrence:", row[3]
        print ":advanced_recurrence:", row[4]
        print ":task_id:", row[5]
        print ":parent_id:", row[6]
        print ":due_date:", row[7]
        print ":END:"
        
        if row[9] !='':
                print row[9].encode('utf8')
        
def main(argv):
    if len(argv)<1:
        print "please call with inputfile name as first parameter"
        sys.exit(1)
    else:
        inputfile = argv[0]

    print "#                  -*- mode: org -*-"
    print "#+TITLE: Import from Appigo Todo"
    print "#+OPTIONS: ^:{}"
    print ""

    convert_tasks(inputfile)
    
if __name__ == "__main__":
   main(sys.argv[1:])
