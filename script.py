import requests
import sys
import json

args = sys.argv[1:]

if len(args) < 1:
    print("argument is missing", file=sys.stderr)
    exit(0)

count = int(args[0])

url = "http://gutendex.com/books"
res = open('books.json', 'w')

books = requests.get(url).json()

books_script = []

# print(books)

for i in range(count):
    book = books['results'][i]
    obj = {}
    obj['title'] = book['title']
    obj['author_name'] = book['authors'][0]['name']
    obj['full_text_pointer'] = [value for key, value in book['formats'].items() if 'text/plain' in key][0]
    books_script.append(obj)

res.write(json.dumps(books_script))
res.close()