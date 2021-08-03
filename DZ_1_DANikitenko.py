#1. (Обязательное) Посмотреть документацию к API GitHub,
#разобраться как вывести список репозиториев для конкретного
#пользователя, сохранить JSON-вывод в файле *.json.

import requests

url = 'https://api.github.com/users/DenNikiten/repos'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

response = requests.get(url, headers=headers)

j_data = response.json()

with open('file1.json', 'wb') as f:
    f.write(response.content)

print('У Дениса Никитенко на github.com следующие репозитории:')
for n in j_data:
    print(n['name'])

