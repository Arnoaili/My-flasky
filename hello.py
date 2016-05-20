from flask import Flask, render_template, session, redirect, url_for,flash, current_app
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import smtplib
from email.mime.text import MIMEText
import MySQLdb
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

mailto_list = 'ai131416@126.com'
mail_host = 'mailsh.tct.tcl.com'
mail_user = 'ta-cd/li.ai' 
mail_pass = 'Arno141516'
mail_postfix='tcl.com'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
    

def send_email(to_list, subject, user):
    content = "User '%s' has joined !" % user
    me = "li.ai" + "@" + mail_postfix
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = to_list
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  
        server.login(mail_user,mail_pass) 
        server.sendmail(me, to_list, msg.as_string())
        server.quit()
        return True
    except Exception, e:
        print str(e)
        return False

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
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
            if send_email(mailto_list, 'New User', form.name.data):
                print 'done!'
        else:
            session['known'] = True
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known = session.get('known'))

if __name__ == '__main__':
    manager.run()
