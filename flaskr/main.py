from flaskr import app
from flask import render_template, request, redirect, url_for
import sqlite3
DATABASE = "database.db"

#一番上のURLにリクエストが来るとindex.htmlを表示する
@app.route('/')
def index():

    date = request.args.get("date")

    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row

    dayevents = con.execute(
        'SELECT * FROM events WHERE date = ? ORDER BY start_time',
        (date,)).fetchall()
    con.close()

    return render_template(
        'index.html',
        date = date,
        dayevents = dayevents
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
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    force_add = request.form.get('force_add')

    if force_add != '1':

        #同じ日付の予定を取得
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        existing_events = con.execute(
            'SELECT * FROM events WHERE date = ?',
            (date,)).fetchall()
        
        con.close()

        #ダブルブッキングのチェック
        for event in existing_events:

            start1 = event["start_time"]
            end1 = event["end_time"]

            start2 = start_time
            end2 = end_time

            if start1 < end2 and start2 < end1:
                return render_template(
                    'add_events.html',
                    warning = True,
                    title = title,
                    date = date,
                    start_time = start_time,
                    end_time = end_time,
                    description = description
                )

    #追加
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

    return redirect(url_for('index', date = date))

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

        return redirect(url_for('index', date = date))

    event = con.execute(
        'SELECT * FROM events WHERE id = ?',
        (event_id,)
    ).fetchone()

    con.close()

    return render_template(
        'edit_events.html',
        event = event
    )

#予定の削除
@app.route('/delete_event')
def delete_event():

    id = request.args.get("id")
    con = sqlite3.connect(DATABASE)

    con.row_factory = sqlite3.Row

    #削除する予定の日付を取得
    event = con.execute(
        'SELECT * FROM events WHERE id = ?',
        (id,)
    ).fetchone()

    #削除
    if event:
        date = event["date"]

    con.execute(
        'DELETE FROM events WHERE id = ?',
        (id,)
        )
    
    con.commit()
    con.close()

    return redirect(url_for('index', date = date))
