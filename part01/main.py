from models import Author, Quote
import connect


def search_by_name(name):
    authors = Author.objects(fullname__istartswith=name)
    for author in authors:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(quote.quote)


def search_by_tag(tag):
    quotes = Quote.objects(tags__istartswith=tag)
    for quote in quotes:
        print(quote.quote)


def search_by_tags(tags):
    tags_list = [tag.strip() for tag in tags.split(',')]
    quotes = Quote.objects(tags__icontains=tags_list[0])
    for tag in tags_list[1:]:
        quotes = quotes.filter(tags__icontains=tag)
    for quote in quotes:
        print(quote.quote)


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
            func(value)
        else:
            print("Невідома команда. Доступні команди: 'name', 'tag', 'tags', 'exit'.")
