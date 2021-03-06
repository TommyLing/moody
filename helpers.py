from datetime import datetime, timedelta
from random import randint

from requests import get, post

from app import db, models
import config

'''
default role = 0
admin role = 1

It defaults to 0 because we don't want to accidentally make a user an admin.
'''
def change_user_role(user_id, role=0):
    query = db.session.query(models.User).filter(models.User.id == user_id)
    user = query.first()

    if user: user.role = role

    db.session.commit()

'''
Send a notifcation to the user.

This method specifies a default message,  but the message can be overriden.
'''
def send_notification(user_id, message='Hey, time to rate your mood for today!'):
    payload = {'access_token' : '{0}|{1}'.format(config.FB_APP_ID,
                                                 config.FB_APP_SECRET),
              'href' : '',
              'template' : message}

    post('https://graph.facebook.com/' + user_id + '/notifications',
         params=payload)

def fake_moods(user_id):
    db.session.query(models.User).\
        filter(models.User.id == user_id).\
        update({"created_date": datetime.utcnow() - timedelta(days=3)})
    db.session.commit()

    query = db.session.query(models.User).filter(models.User.id == user_id)
    user = query.first()

    t = user.created_date
    i = 0

    while i < 1:
        mood = models.Mood(rating=randint(1,10), hospital=1, medication=1,
                           time_stamp=(t + timedelta(hours=24*i)))

        user.moods.append(mood)
        i += 1

    db.session.commit()
