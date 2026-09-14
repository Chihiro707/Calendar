from flaskr import app
from datetime import datetime
from flask import render_template, request, redirect, url_for
import sqlite3
DATABASE = "database.db"

#一番上のURLにリクエストが来るとindex.htmlを表示する
@app.route('/')
def index():

    con = sqlite3.connect(DATABASE)
    db_events = con.execute('SELECT * from events').fetchall()
    con.close()

    events = []
    for row in db_events:
        events.append({'title':row[0], 'date':row[1], 'start_time':row[2], 'end_time':row[3], 'description':row[4]})

    return render_template(
        'index.html',
        events = events
    )

#add_eventsのURLにリクエストが来るとadd_events.htmlを表示する
@app.route('/add_events')
def add_events():

    return render_template(
        'add_events.html'
    )

#予定の追加リクエストが来ると対応する
@app.route('/add', methods = ['POST'])
def add():

    title = request.form['title']

    date = request.form['date']
    dt = datetime.strptime(date, "%Y-%m-%d")
    year = dt.year
    month = dt.month
    day = dt.day

    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    
    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO events VALUES(?, ?, ?, ?, ?)',
                [title, date, start_time, end_time, description])
    con.commit()
    con.close()

    return redirect(url_for('index'))

#add_eventsのURLにリクエストが来るとadd_events.htmlを表示する
@app.route('/edit_events')
def edit_events():

    return render_template(
        'edit_events.html'
    )

@app.route('/events')
def events():

    date = request.args.get("date")
    con = sqlite3.connect(DATABASE)

    con.row_factory = sqlite3.Row
    events = con.execute('SELECT * FROM events where date = ?',(date,)).fetchall()

    con.close()

    return render_template(
        "index.html",
        date=date,
        events=events
        )