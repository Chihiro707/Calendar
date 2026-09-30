from flaskr import app
from flaskr.holiday import get_holidays
from flaskr.db import add_event, get_dates_with_events, get_events_by_date, get_event_by_id, update_event, delete_event
from flask import render_template, request, redirect, url_for

#一番上のURLにリクエストが来るとindex.htmlを表示する
@app.route('/')
def index():

    date = request.args.get("date")

    event_dates = get_dates_with_events()
    event_dates = [row["date"] for row in event_dates]
    dayevents = get_events_by_date(date)

    holidays = get_holidays()

    return render_template(
        'index.html',
        date = date,
        event_dates = event_dates,
        dayevents = dayevents,
        holidays = holidays
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
        existing_events = get_events_by_date(date)

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
    add_event(title, date, start_time, end_time, description)

    return redirect(url_for('index', date = date))

#予定の編集が行われたときに反応する
@app.route('/edit/<int:event_id>', methods=['GET','POST'])
def edit_event(event_id):

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        description = request.form['description']

        update_event(event_id, title, date, start_time, end_time, description)

        return redirect(url_for('index', date = date))

    event = get_event_by_id(event_id)

    return render_template(
        'edit_events.html',
        event = event
    )

#予定の削除
@app.route('/delete_event')
def delete_event():

    id = request.args.get("id")
    date = get_dates_with_events(id)
    date = date["date"]

    delete_event(id)

    return redirect(url_for('index', date = date))
