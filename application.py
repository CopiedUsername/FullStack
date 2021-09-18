# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 21:14:20 2019

@author: Cole Bohanon
"""
from flask import Flask, render_template, make_response, request, redirect, url_for, flash, send_file, session, escape
import sqlite3 as sql 
import csv
import time

application = Flask(__name__)
application.secret_key = 'ColesSuperSecretKey'
# When user enters in localhost:5000 and hits enter, they will be redirected immediately to the manage students page
@application.route("/")
def home():
   if 'username' in session:
      return redirect(url_for('students'))
   else:    
       return redirect(url_for('form'))
#First page the user will see
@application.route('/login', methods = ['GET', 'POST'])
def login():
   con = sql.connect("FBLA2.db")
   if request.method == 'POST':
      session['username'] = request.form['username']
      session['password'] = request.form['password']
      if (session['username'] == '123admin') and (session['password'] == '56789'):
          con = sql.connect("FBLA2.db")
          cur = con.cursor()
          cur.execute("UPDATE login SET loggedin = ?", [1] )
          con.commit()
          return redirect(url_for('students'))
      else:
          flash("Incorrect login, please try again")
          return redirect(url_for('form'))
@application.route('/logout', methods = ['GET', 'POST'])
def logout():
   con = sql.connect("FBLA2.db")
   cur = con.cursor()
   cur.execute("UPDATE login SET loggedin = ?", [0] ) 
   con.commit()
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('home'))
@application.route('/students')
def students():
   if 'username' in session: 
       con = sql.connect("FBLA2.db")
       con.row_factory = sql.Row
       cur = con.cursor()
       cur.execute("select * from students, login")
       rows = cur.fetchall();
       return render_template("students.html",rows = rows)
   else:
       return redirect(url_for('form'))
#This will run when the user clicks add in the students screen
#This will get the data values from the html form and plug them into the database using INSERT
@application.route("/post_data", methods=['GET', 'POST'])
def post_data():
    try:
     if request.method == 'POST':
      first = request.form['first']
      last = request.form['last']
      gradelevel = request.form['gradelevel']
      student_id = request.form['student_id']
      with sql.connect("FBLA2.db") as con:
          cur = con.cursor()
          cur.execute("INSERT INTO students (first,last,gradelevel,student_id) VALUES (?,?,?,?)",(first,last,gradelevel,student_id) )
          con.commit()
          flash("Record added successfully!")
    except:
     con.rollback()
     
     flash("There is already a student with that ID")
          
    return redirect(url_for('students'))
#This will run when the user clicks remove in the manage students screen
#This will remove whatever row that has the specific student ID the user wishes to remove      
@application.route("/rem_data", methods=['POST'])
def rem_data():
    if request.method == 'POST':
        student_id = request.form['student_id']
        with sql.connect("FBLA2.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM students WHERE student_id = ?", [student_id] )
            con.commit()
            flash("Record removed successfully!")
            return redirect(url_for('students'))
#This will run when the user clicks update in the manage students screen
#This will get a hidden value, row_id, from the table in the form and update that specific
#row to whatever values the user desires. The user is not able to edit the row id      
@application.route("/upd_data", methods=['POST'])
def upd_data():
    try:
     if request.method == 'POST':
      first = request.form['first']
      last = request.form['last']
      gradelevel = request.form['gradelevel']
      student_id = request.form['student_id']
      row_id = request.form['row_id']
      with sql.connect("FBLA2.db") as con:
          cur = con.cursor()
          cur.execute("UPDATE students SET first = ?,last = ?,gradelevel = ?,student_id = ? WHERE row_id = ?", [first,last,gradelevel,student_id,row_id])
          con.commit()
          flash("Record updated successfully!")
    except:
        con.rollback()
     
        flash("There is already a student with that ID")
    return redirect(url_for('students'))
#This is the manage books screen      
@application.route("/books")
def books():
    if 'username' in session:
        con = sql.connect("FBLA2.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from ebooks")
        rows = cur.fetchall();
        return render_template('books.html',rows = rows)
    else:
        return redirect(url_for('form'))
#This will run when the user clicks add in the manage books screen
#This will insert datavalues into the database, however, it will return an error
#if a book is associated with an ID twice. A simple flash message will appear on screen
#notifying the user that the book already exists      
@application.route("/post_ebook", methods=['POST'])
def post_ebook():
    try:
        if request.method == 'POST':
            ebooktitle = request.form['ebooktitle']
            ebook_id = request.form['ebook_id']
            with sql.connect("FBLA2.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO ebooks (ebooktitle,ebook_id) VALUES (?,?)",(ebooktitle,ebook_id) )
                con.commit()
                flash("Record added successfully!")
    except:
     con.rollback()
     flash("Book ID or title already exists")
          
    return redirect(url_for('books'))
#This will run when the user clicks remove in the manage books screen
#This will remove data from the database in the row that contains the ebook ID specified
#since the ebook ID can be only used once
@application.route("/rem_ebook", methods=['POST'])
def rem_ebook():
    if request.method == 'POST':
      ebook_id = request.form['ebook_id']
      with sql.connect("FBLA2.db") as con:
          cur = con.cursor()
          cur.execute("DELETE FROM ebooks WHERE ebook_id = ?", [ebook_id] )
          con.commit()
          flash("Record removed successfully!")
          return redirect(url_for('books'))
#This will run when the user clicks update in the manage books screen
#This will get a hidden row ID from the table and update the specific row the user
#wishes to update. An error occurs when the user attempts to assign two books to one ID     
@application.route("/upd_ebook", methods=['POST'])
def upd_ebook():
    try:
     if request.method == 'POST':
      ebooktitle = request.form['ebooktitle']
      ebook_id = request.form['ebook_id']
      row_id = request.form['row_id']
      with sql.connect("FBLA2.db") as con:
          cur = con.cursor()
          cur.execute("UPDATE ebooks SET ebooktitle = ?,ebook_id = ? WHERE row_id = ?", (ebooktitle,ebook_id,row_id))
          con.commit()
          flash("Record updated successfully!")

    except:
     con.rollback()
     flash("Book ID or title already exists")
          
    return redirect(url_for('books'))
      
@application.route("/codes")
def codes():
    if 'username' in session:
        con = sql.connect("FBLA2.db")
        con.row_factory = sql.Row 
        cur = con.cursor()
        cur.execute("select ebook_redemptioncodes.redemptioncode,ebook_redemptioncodes.ebook_id,ebooks.ebooktitle,ebook_redemptioncodes.student_id, ebook_redemptioncodes.row_id from ebook_redemptioncodes join ebooks on ebooks.ebook_id = ebook_redemptioncodes.ebook_id")
        rows = cur.fetchall();
        return render_template('codes.html',rows = rows)
    else: 
        return redirect(url_for('form'))

@application.route("/post_red", methods=['POST'])
def post_red():
    try:
        if request.method == 'POST':
            redemptioncode = request.form['redemptioncode']
            ebook_id = request.form['ebook_id']
            student_id = request.form['student_id']
        with sql.connect("FBLA2.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO ebook_redemptioncodes (redemptioncode,ebook_id,student_id) values(?,?,IFNULL(NULLIF(TRIM(?),''),'Available'))",(redemptioncode,ebook_id, student_id) )
            con.commit()
            flash("Record successfully added!")
            return redirect(url_for('codes'))
    except:
     con.rollback()
     flash("This redemption code already exists!")
          
    return redirect(url_for('codes'))
@application.route("/rem_red", methods=['POST'])
def rem_red():
    if request.method == 'POST':
      redemptioncode = request.form['redemptioncode']
      with sql.connect("FBLA2.db") as con:
          cur = con.cursor()
          cur.execute("DELETE FROM ebook_redemptioncodes WHERE redemptioncode = ?", [redemptioncode] )
          con.commit()
          flash("Record successfully removed!")
          return redirect(url_for('codes'))
      
@application.route("/report", methods=['POST','GET'])    
def report():

    conn = sql.connect('FBLA2.db')
    cur = conn.cursor()


    sqlSelect = ("SELECT ebooks.ebooktitle, ebook_redemptioncodes.redemptioncode, students.student_id, students.first, students.last,ebook_redemptioncodes.timestamp "
                 " FROM ebook_redemptioncodes "
                 " inner join ebooks "
                 " on ebooks.ebook_id = ebook_redemptioncodes.ebook_id "
                 " inner join students "
                 " on students.student_id = ebook_redemptioncodes.student_id "
		         " WHERE date(timestamp) between date('now','-7 days') and date('now')")
    try:
        results = cur.execute(sqlSelect)
    except:
        flash("Ebook Report Failed!")
    conn.commit() 

    header = ["EBOOK","REDEMPTION CODE","ASSIGNED STUDENT ID","STUDENT FIRST NAME","STUDENT LAST NAME","REDEMPTION_DATE"]
     
    with open('report.csv','wt', newline='') as out:
        w=csv.writer(out,delimiter=',')
        w.writerow(i for i in header)
        for r in results.fetchall():
            w.writerow(r)
    
    return send_file('report.csv',mimetype='text/csv',attachment_filename='report.csv',as_attachment=True) 

@application.route("/upd_red", methods=['POST'])
def upd_red():
    try:
        redemptioncode = request.form['redemptioncode']
        ebook_id = request.form['ebook_id']
        student_id = request.form['student_id']
        row_id = request.form['row_id']
        with sql.connect("FBLA2.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE ebook_redemptioncodes SET redemptioncode = ?,ebook_id = ?, student_id = ?, timestamp = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW') WHERE row_id = ?", (redemptioncode,ebook_id,student_id,row_id))
            con.commit()
            flash("Record successfully updated!")
    except:
        flash("This redemption code already exists!")
    return redirect(url_for('codes'))
@application.route("/form", methods=['POST', 'GET'])
def form():
    return render_template('form.html')
#@application.route("/login", methods=['GET', 'POST'])
#def login():
#        username = request.form['username']
#        password = request.form['password']
#        if username != '123admin' or password != '56789':
#            flash('Invalid Credentials. Please try again.')
#            return redirect(url_for('form'))
#        else:
#            flash('Login successful!')
#            time.sleep(3)
#            con = sql.connect("FBLA2.db")
#            cur = con.cursor()
#            cur.execute("UPDATE login SET loggedin = ?", [1] )
#            con.commit()
#            return redirect(url_for('students'))
#@application.route("/logout", methods=['GET', 'POST'])
#def logout():
#            con = sql.connect("FBLA2.db")
#            cur = con.cursor()
#            cur.execute("UPDATE login SET loggedin = ?", [0] )
#            con.commit()
#            return redirect(url_for('students'))
@application.route("/wtemplate", methods=['GET', 'POST'])
def wtemplate():
    if request.method == "POST":
        url = request.form['url']
        con = sql.connect("FBLA2.db")
        cur = con.cursor()
        cur.execute("UPDATE login SET templatecolor = ?", ['w'] )
        con.commit()
        return redirect(url_for(url))
@application.route("/btemplate", methods=['GET', 'POST'])
def btemplate():
    if request.method == "POST":
        url = request.form['url']
        con = sql.connect("FBLA2.db")
        cur = con.cursor()
        cur.execute("UPDATE login SET templatecolor = ?", ['b'] )
        con.commit()
        return redirect(url_for(url))


if __name__ == "__main__":

    application.run(debug = True)
    
