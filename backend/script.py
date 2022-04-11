import requests
import sys
import json

args = sys.argv[1:]

if len(args) < 1:
    print("argument is missing", file=sys.stderr)
    exit(0)

count = int(args[0])

url = "http://gutendex.com/books/?page="
res = open('books.json', 'w')

page_number = count // 32
if count % 32 > 0:
    page_number += 1



books_script = []
for i in range(1, page_number+1):
    books = requests.get(url + str(page_number)).json()

    j = 0
    while j < 32 and (((i - 1) * 32) + j) < count:
        book = books['results'][j]
        obj = {}
        obj['title'] = book['title']
        obj['author_name'] = book['authors'][0]['name']
        obj['full_text_pointer'] = [value for key, value in book['formats'].items() if 'text/plain' in key][0]
        obj['subjects'] = book['subjects']
        books_script.append(obj)
        j += 1

res.write(json.dumps(books_script))
res.close()