import requests
from itertools import count
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os


def predict_rub_salary(salary_from = None,salary_to = None):
    if salary_from and salary_to:
        average_salary = int((salary_from+salary_to)/2)
    elif salary_from:
        average_salary = int(salary_from * 1.2)
    elif salary_to:
        average_salary = int(salary_to * 0.8)
    else:
        average_salary = None
    return average_salary


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
    vacancies_found = {}
    langs = [
        "python",
        "java",
    ]
    for lang in langs:
        salary_vacancies=[]
        for page in count(0):
            vacancies = get_vacancies_hh(lang, page=page)
            if page >= vacancies['pages']-1:
                break
            for vacancy in vacancies["items"]:
                salary = vacancy.get("salary")
                if salary and salary["currency"] == "RUR":
                    predicted_salary = predict_rub_salary(vacancy["salary"].get("from"),vacancy["salary"].get("to"))
                if predicted_salary:
                    salary_vacancies.append(predicted_salary)
        average_salary = None
        if salary_vacancies:
            average_salary = int(sum(salary_vacancies)/len(salary_vacancies)) 
            
        vacancies_found[lang] = {
            "vacancies_found": vacancies["found"],
            "vacancies_processed": len(salary_vacancies),
            "average_salary": average_salary,
        }
    return vacancies_found


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
    vacancies_found = {}
    langs = [
        "python",
        "java",
        "javascript",
        "ruby",
        "php",
        "c++",
        "c#",
        "C",
    ]
    for lang in langs:
        salary_vacancies=[]
        for page in count(0,1):
            vacancies = get_vacancies_sj(sj_key, lang, page=page,)
            if not vacancies['objects']:
                break
            for vacancy in vacancies["objects"]:
                predicted_salary = predict_rub_salary(vacancy["payment_from"],vacancy["payment_to"])
                if predicted_salary:
                    salary_vacancies.append(predicted_salary)
        average_salary = None
        if salary_vacancies:
            average_salary = int(sum(salary_vacancies)/len(salary_vacancies)) 
            
        vacancies_found[lang] = {
            "vacancies_found": vacancies["found"],
            "vacancies_processed": len(salary_vacancies),
            "average_salary": average_salary,
        }
    return vacancies_found


def  create_table(title,statistics):
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    for lang, vacancies in statistics.items():
        table_data.append([lang,vacancies["vacancies_found"],vacancies["vacancies_processed"],vacancies["average_salary"]])
    table = AsciiTable(table_data, title)
    return table.table


def main():
    load_dotenv()
    sj_key = os.environ["SJ_KEY"]
    print(create_table("hh Moscow",get_statistic_hh()))
    print(create_table("sj Moscow",get_vacancies_sj(sj_key)))
    
    
if __name__ == "__main__":
    main()
    