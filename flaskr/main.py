from flaskr import app
from datetime import datetime
from flask import render_template, request, redirect, url_for
import sqlite3
DATABASE = "database.db"

#一番上のURLにリクエストが来るとindex.htmlを表示する
@app.route('/')
def index():

    return render_template(
        'index.html'
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
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    
    con = sqlite3.connect(DATABASE)
    con.execute("""
        INSERT INTO events(
            title,
            date,
            start_time,
            end_time,
            description
        )
        VALUES(?, ?, ?, ?, ?)
        """,(
            title,
            date,
            start_time,
            end_time,
            description
        ))

    con.commit()
    con.close()

    return redirect(url_for('index'))

#edit_eventsのURLにリクエストが来るとedit_events.htmlを表示する
@app.route('/edit_events')
def edit_events():

    return render_template(
        'edit_events.html'
    )

#カレンダー上の日付をクリックすると反応する
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
        dayevents=events
        )

#予定の編集が行われたときに反応する
@app.route('/edit/<int:event_id>', methods=['GET','POST'])
def edit_event(event_id):

    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        description = request.form['description']

        con.execute("""
            UPDATE events
            SET title = ?,
                date = ?,
                start_time = ?,
                end_time = ?,
                description = ?
            WHERE id = ?
        """,(
            title,
            date,
            start_time,
            end_time,
            description,
            event_id
        ))

        con.commit()
        con.close()

        return redirect(url_for('index'))

    event = con.execute(
        'SELECT * FROM events WHERE id = ?',
        (event_id,)
    ).fetchone()

    con.close()

    return render_template(
        'edit_events.html',
        event = event
    )

@app.route('/delete/<int:event_id>', methods = ['POST'])
def delete_event(event_id):
    
    con = sqlite3.connect(DATABASE)
    
    con.execute(
        'DELETE FROM events WHERE id = ?',
        (event_id,)
    )

    con.commit()
    con.close()

    return redirect(url_for('index'))