# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 19:20:18 2019

@author: Jason.Bohanon
"""

import sqlite3
import csv
#establish a connection to the database
db = sqlite3.connect('fbla2.db')
cur = db.cursor()

#set a big sqlite command to a variable
sql = ''' SELECT ebooktitle, r.redemptioncode, s.student_id, s.first, s.last,r.timestamp 
                           FROM ebook_redemptioncodes r 
                            	inner join ebooks e
                                    on e.ebook_id = r.ebook_id
                            	inner join students s 
                            		on s.student_id = r.student_id'''
results = cur.execute(sql)
db.commit() 
#sets the header for the columns in the report file
header = ["EBOOK","REDEMPTION CODE","ASSIGNED STUDENT ID","STUDENT FIRST NAME","STUDENT LAST NAME","REDEMPTION_DATE"]
#opens report file and clears it of all data and writes new data to the file
with open('report.csv','wt', newline='') as out:
    w=csv.writer(out,delimiter=',')
    w.writerow(i for i in header)
    for r in results.fetchall():
        w.writerow(r)
