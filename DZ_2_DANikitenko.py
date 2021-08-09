from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

#https://ekaterinburg.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=Data+science&from=suggest_post&page=0

url = 'https://ekaterinburg.hh.ru'
url2 = '?area=&fromSearchLine=true&st=searchVacancy&text=Data+science&from=suggest_post&page=0'
# params = {'area':'',
#           'fromSearchLine':'true',
#           'st':'searchVacancy',
#           'text':'Data+science',
#           'from':'suggest_post',
#           'page':'0'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

response = requests.get(url+'/search/vacancy'+url2, headers=headers)

soup = bs(response.text, 'html.parser')

vacancies_list = soup.find_all('div', {'class':'vacancy-serp-item'})

vacancies = []
for vacancy in vacancies_list:
    vacancy_data = {}
    vacancy_info = vacancy.find('span', {'class':'g-user-content'})
    vacancy_name = vacancy_info.getText()
    vacancy_url_pre = vacancy_info.findChild()
    vacancy_url = vacancy_url_pre['href']
    employer_info = vacancy.find('a', {'data-qa':'vacancy-serp__vacancy-employer'})
    employer_url = url + employer_info['href']

    salary_min = None
    salary_max = None
    currency_salary = None
    try:
        vacancy_salary_info = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        vacancy_salary = vacancy_salary_info.getText().split()
        if vacancy_salary[0] == 'от':
            salary_min = int(f'{vacancy_salary[1]}{vacancy_salary[2]}')
        elif vacancy_salary[0] == 'до':
            salary_max = int(f'{vacancy_salary[1]}{vacancy_salary[2]}')
        else:
            salary_min = int(f'{vacancy_salary[0]}{vacancy_salary[1]}')
            salary_max = int(f'{vacancy_salary[3]}{vacancy_salary[4]}')
        currency_salary = vacancy_salary[-1]
    except:
        pass

    vacancy_data['name'] = vacancy_name
    vacancy_data['url'] = vacancy_url
    vacancy_data['url_emp'] = employer_url
    vacancy_data['salary_min'] = salary_min
    vacancy_data['salary_max'] = salary_max
    vacancy_data['salary_currency'] = currency_salary

    vacancies.append(vacancy_data)


df = pd.DataFrame(vacancies)
df.to_json('vacancy_list.json')
df.to_csv('vacancy_list.csv')

df = pd.read_csv('vacancy_list.csv')
print(df)

