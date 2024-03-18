import requests
from itertools import count
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os


def predict_rub_salary(salary_from = None,salary_to = None):
    if salary_from and salary_to:
        everage_sallary = int((salary_from+salary_to)/2)
    elif salary_from:
        everage_sallary = int(salary_from * 1.2)
    elif salary_to:
        everage_sallary = int(salary_to * 0.8)
    else:
        everage_sallary = None
    return everage_sallary


def get_vacancies_hh(language, page=0):
    url = "https://api.hh.ru/vacancies" 
    area = 1
    params = {
        "text": language,
        "area": area,
        "page": page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_statistic_hh():
    found_vacancy = {}
    langs = [
    "python","java",
    ]
    for lang in langs:
        salary_vacancyes=[]
        for page in count(0):
            vacancyes = get_vacancies_hh(lang, page=page)
            if page >= vacancyes['pages']-1:
                break
            for vacancy in vacancyes["items"]:
                salary = vacancy.get("salary")
                if salary and salary["currency"] == "RUR":
                    get_predict_salary = predict_rub_salary(vacancy["salary"].get("from"),vacancy["salary"].get("to"))
                if get_predict_salary:
                    salary_vacancyes.append(get_predict_salary)
        everage_salary = None
        if salary_vacancyes:
            everage_salary = int(sum(salary_vacancyes)/len(salary_vacancyes)) 
            
        found_vacancy[lang] = {
            "vacancies_found": vacancyes["found"],
            "vacancies_processed": len(salary_vacancyes),
            "average_salary": everage_salary,
        }
    return found_vacancy


def get_vacancies_sj(sj_key, lang, page=0): 
    url_sj = "https://api.superjob.ru/2.0/vacancies/"

    headers = {
        "X-Api-App-Id": sj_key
    }

    params = {
        "town":  "Moscow",
        "keyword": f"Программист {lang}",
        "page": page,
    }
    response = requests.get(url_sj, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

    
def predict_rub_salary_for_superJob(sj_key):
    found_vacancy = {}
    langs = [
    "python","java","javascript","ruby","php","c++","c#","C",
   ]
    for lang in langs:
        salary_vacancyes=[]
        for page in count(0,1):
            vacancyes = get_vacancies_sj(sj_key, lang, page=page,)
            if page in vacancyes['objects']:
                break
            for vacancy in vacancyes["objects"]:
                get_predict_salary = predict_rub_salary(vacancy["payment_from"],vacancy["payment_to"])
                if get_predict_salary:
                    salary_vacancyes.append(get_predict_salary)
        everage_salary = None
        if salary_vacancyes:
            everage_salary = int(sum(salary_vacancyes)/len(salary_vacancyes)) 
            
        found_vacancy[lang] = {
            "vacancies_found": vacancyes["found"],
            "vacancies_processed": len(salary_vacancyes),
            "average_salary": everage_salary,
        }
    return found_vacancy


def  create_table(title,statistics):
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    for lang, vacancyes in statistics.items():
        table_data.append([lang,vacancyes["vacancies_found"],vacancyes["vacancies_processed"],vacancyes["average_salary"]])
    table = AsciiTable(table_data, title)
    return table.table


def main():
    load_dotenv()
    sj_key = os.environ["SJ_KEY"]
    print(create_table("hh Moscow",get_statistic_hh()))
    print(create_table("sj Moscow",get_vacancies_sj(sj_key)))
    
    
if __name__ == "__main__":
    main()
    