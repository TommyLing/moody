from app import db, models
from random import randint
from datetime import datetime, timedelta
i = 0

query_id = 1

query = db.session.query(models.User).filter(models.User.id == query_id)
user = query.first()
user.moods = []
t = datetime.utcnow() + timedelta(hours=24*3)
while i < 20:
    user.moods.append(
        models.Mood(rating= randint(1,10), time_stamp=(t - timedelta(hours=24*i)))
    )
    i += 1

db.session.commit()
