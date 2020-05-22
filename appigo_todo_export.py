
import sys
import sqlite3

class Converter(object):
    """loads values from database and writes as org-mode formatted text to stdout"""

    def load(self,dbname):
        """opens database file with name dbname"""
     
        connection = sqlite3.connect(dbname)
        cursor = connection.cursor()
        cursor.execute("select name,type,type_data,recurrence,advanced_recurrence from tasks where deleted=0 and completion_date=-62135769600.0 order by parent_id") 
        print("fetchall:")
        result = cursor.fetchall() 
        for r in result:
            self.convert(r)
        connection.close()

    tasktype = {
        0:"task",
        1: "project",
        2: "contact",
        6: "url"
        }
       
    def convert(self,row):
        """converts a single task row"""
  #      print row
        print "** TODO ", row[0].encode('utf-8')
        print ":PROPERTIES:"
        print ":Tasktype:"+Converter.tasktype[row[1]]
        print ":type_data:", row[2].encode('utf-8')
        print ":recurrence:", row[3]
        print ":advanced_recurrence:", row[4]

        print ":END:"
        print ""
        
def main(argv):
    if len(argv)<1:
        inputfile ="x"
    else:
        inputfile = argv[0]

    print inputfile
    converter = Converter()
    converter.load(inputfile)
    
if __name__ == "__main__":
   main(sys.argv[1:])
