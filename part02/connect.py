from mongoengine import connect
import configparser
import certifi

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True,
        tlsCAFile=certifi.where())

try:
    connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""",
            ssl=True,
            tlsCAFile=certifi.where())
    print("Підключення до MongoDB відбулось успішно.")
except Exception as e:
    print(f"Помилка підключення до MongoDB: {str(e)}")
