import connect
import json
from models import Author, Quote

with open('authors.json', 'r', encoding='utf-8') as authors_file:
    authors_data = json.load(authors_file)

for author_data in authors_data:
    author = Author(**author_data)
    author.save()

with open('quotes.json', 'r', encoding='utf-8') as quotes_file:
    quotes_data = json.load(quotes_file)

for quote_data in quotes_data:
    author_fullname = quote_data['author']
    author = Author.objects(fullname=author_fullname).first()

    if author:
        quote_data['author'] = author
        quote = Quote(**quote_data)
        quote.save()
    else:
        print(f'Автор {author_fullname} не знайдений. Цитата не була збережена.')
