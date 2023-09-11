import redis
from redis_lru import RedisLRU
from models import Author, Quote
import connect

client = redis.Redis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_by_name(name):
    authors = Author.objects(fullname__istartswith=name)
    quotes_by_name = []
    for author in authors:
        quotes_by_name.extend(Quote.objects(author=author))
    return [quote.quote for quote in quotes_by_name]


@cache
def search_by_tag(tag):
    quotes_by_name = Quote.objects(tags__istartswith=tag)
    return [quote.quote for quote in quotes_by_name]


@cache
def search_by_tags(tags):
    tags_list = [tag.strip() for tag in tags.split(',')]
    quotes = Quote.objects(tags__icontains=tags_list[0])
    for tag in tags_list[1:]:
        quotes_by_tags = quotes.filter(tags__icontains=tag)
    return [quote.quote for quote in quotes_by_tags]


commands = {
    'name': search_by_name,
    'tag': search_by_tag,
    'tags': search_by_tags,
}

if __name__ == '__main__':

    while True:
        user_input = input(
            "Введіть команду (наприклад, 'name: Steve Martin', 'tag: life', 'tags: life,live', 'exit'): ").strip()

        if user_input == 'exit':
            break

        parts = user_input.split(':')
        if len(parts) != 2:
            print("Некоректний формат команди. Введіть команду у форматі 'команда: значення'.")
            continue

        command, value = parts[0].strip(), parts[1].strip()

        # Виклик відповідної функції за допомогою словника команд
        func = commands.get(command)
        if func:
            results = func(value)
            for result in results:
                print(result)

        else:
            print("Невідома команда. Доступні команди: 'name', 'tag', 'tags', 'exit'.")
