import sqlite3 as sql
from flask import Flask, request, jsonify, render_template, url_for, flash, redirect, make_response, Response
from model import *
import datetime
import io
import csv



# define the app
app = Flask(__name__)


#error page 
# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404

#home page    
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/inference', methods=['POST', 'GET'])
def inference():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        dob =request.form['dob']
        history = request.form['history']
        favc = request.form['favc']
        fcvc = request.form['fcvc']
        ncp = request.form['ncp']
        caec = request.form['caec']
        smoke = request.form['smoke']
        ch2o = request.form['ch2o']
        scc = request.form['scc']
        faf = request.form['faf']
        tue = request.form['tue']
        calc = request.form['calc']
        mtrans = request.form['mtrans']

        if not name:
            flash('Please enter a name')
        else:
            
            dob = datetime.datetime.strptime(dob, "%m/%d/%Y")
            year1 = datetime.date.today().year
            year2 = dob.year
            age = year1 - year2

            obese = obPredict(gender,age,history, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans)
           
            x = datetime.datetime.now()
            date = x.ctime()

            value = obese
        # now we establish our connection
            with sql.connect("history.db") as con:
                    cur = con.cursor()
                    
                    cur.execute("INSERT INTO Results(date, name, gender,age,history, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans, value) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(date,name, gender,age,history, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans, value))

                    con.commit()
                       
            return render_template('inference.html', obese = obese)
    return render_template('inference.html')


@app.route("/model")
def model():
    return render_template('model.html')

@app.route("/history")
def history():
    con = sql.connect("history.db") 
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select date, name, age, value from results")
    rows = cur.fetchall()
    return render_template('history.html', rows = rows)


@app.route('/download')
def download():
    con = sql.connect("history.db") 
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select date, name, age, value from results")
    result = cur.fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    line = ['Date, Name, Age, Classification']
    writer.writerow(line)

    for row in result:
        line = [row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3]]
        writer.writerow(line)
    
    output.seek(0)
    con.close()
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=patienthistory.csv"})

if __name__ == "__main__":   
    app.run(host='0.0.0.0')