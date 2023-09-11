from mongoengine import *
import certifi

connect(db='DB',
        host=f"""mongodb+srv://user:user@cluster0.ardcnka.mongodb.net/?retryWrites=true&w=majority""", ssl=True,
        tlsCAFile=certifi.where()
        )


class User(Document):
    fullname = StringField(max_length=50)
    email = StringField(required=True)
    phone_number = StringField(max_length=15)
    notification_method = StringField(choices=['SMS', 'email'])
    completed = BooleanField(default=False)
    meta = {"collections": "tasks"}
