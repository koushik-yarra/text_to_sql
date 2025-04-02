import sqlite3


conn=sqlite3.connect("student.db")
cursor=conn.cursor()

table_info="""Create table if not exists student(id,name varchar(25),class varchar(25),marks int(4))"""
cursor.execute(table_info)


# insert some more records

cursor.execute("""insert into student values(1,'John', '10th', 85)""")
cursor.execute("""insert into student values(2,'Jane', '10th', 90)""")
cursor.execute("""insert into student values(3,'Doe', '9th', 78)""")
cursor.execute("""insert into student values(4,'Smith', '8th', 88)""")
cursor.execute("""insert into student values(19,'Amelia', '9th', 81)""")    
cursor.execute("""insert into student values(20,'Elijah', '8th', 83)""")
cursor.execute("""insert into student values(21,'Harper', '7th', 90)""")
cursor.execute("""insert into student values(45,'Sofia', '7th', 67)""")



print("Data inserted is")
data=cursor.execute("SELECT * FROM student")

for row in data:
    print(row)


conn.commit()
conn.close()
