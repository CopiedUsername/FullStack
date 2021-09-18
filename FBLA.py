import sqlite3

conn = sqlite3.connect('FBLA2.db')

cur = conn.cursor()
#create students table and prevents the student ID column from having the same value from being entered more than once
cur.execute('''CREATE TABLE IF NOT EXISTS students(
                row_id integer primary key autoincrement,
                first text,
                last text,
                student_id integer,
                gradelevel integer,
                unique(student_id),
                check(9 <= gradelevel AND gradelevel <= 12)
            )''')
conn.commit()
#create ebooks table and prevents ebooktitle and ebook ID from having the same value from being entered more than once
cur.execute('''CREATE TABLE IF NOT EXISTS ebooks(
                row_id integer primary key autoincrement,
                ebooktitle text,
                ebook_id real,
                unique(ebook_id)
            )''')
conn.commit()
#creates ebook redemptioncodes and prevents the redemptioncode from having the same value from being entered more than once
cur.execute('''CREATE TABLE IF NOT EXISTS ebook_redemptioncodes (
                row_id integer primary key autoincrement,
                redemptioncode integer,
                ebook_id integer,
                student_id integer null,
                timestamp datetime default current_timestamp,
                unique(redemptioncode)
            )''')
conn.commit()
cur.execute('''CREATE TABLE IF NOT EXISTS login (
               loggedin integer,
               templatecolor text
            )''')
#inserts values into students
cur.execute('''INSERT OR IGNORE INTO students (first, last, student_id, gradelevel) 
            VALUES ('Charley', 'Schmitt', 1, 9),
            ('Arnold', 'Seay', 2, 10),
            ('Ashley', 'Toombs', 3, 12),
            ('John', 'Hawk', 4, 9),
            ('Nathan', 'Moore', 5, 11)''') 
conn.commit()
#inserts values into ebooks
cur.execute('''INSERT OR IGNORE INTO ebooks (ebooktitle, ebook_id)
            VALUES ('Monsters of Men', '13x401'),
            ('Poisonwood Bible', '21x182'),
            ('Monsters of Men', '38x819'),
            ('A Brief History of Time', '44x019'),
            ('A Midsummer Nights Dream', '50x001')''')
conn.commit()
#inserts values into ebook redemptioncodes
cur.execute('''INSERT OR IGNORE INTO ebook_redemptioncodes (redemptioncode, ebook_id, student_id, timestamp)
            VALUES (9257354, '13x401', 1, date('now')),
            (8400380, '38x819', 2, '2019-01-31'),
            (1039710, '50x001', 1, '2019-02-20'),
            (9134106, '44x019', NULL, NULL),
            (6113151, '21x182', NULL, NULL)''')
conn.commit()
cur.execute('''INSERT OR IGNORE INTO login (loggedin, templatecolor)
            VALUES (1, 'b')''')
conn.commit()
#conn.close()


