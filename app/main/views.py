from flask import render_template, session, redirect, url_for,flash
from ..emails import send_email
from . import main
from .forms import NameForm
from config import config
import MySQLdb

@main.route('/', methods=['GET', 'POST'])
def index():
    conn = MySQLdb.connect(user='root',passwd='admin0',host='localhost')
    conn.select_db('user')
    curr = conn.cursor()
    curr.execute('select name from person')
    listz = []
    for row in curr.fetchall():
        for a in row:
            listz.append(a)

    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        if form.name.data not in listz:
            curr.execute('insert into person(name) values("%s")' % (form.name.data))
            conn.commit()
            session['known'] = False
            #print config['default'].mailto_list
            if send_email(config['default'].mailto_list, 'New User', form.name.data):
                print 'done!'
        else:
            session['known'] = True
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'), known = session.get('known'))
