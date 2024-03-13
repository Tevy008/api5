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


def vocancy_hh(language, page=0):
    url = "https://api.hh.ru/vacancies" 
    params = {
        "text": language,
        "area": 1,
        "page": page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_statistic_hh():
    found_vocancy = {}
    langs = [
    "python","java",
    ]
    for lang in langs:
        salary_vocancy=[]
        for page in count(0):
            vocancyes = vocancy_hh(lang, page=page)
            if page >= vocancyes['pages']-1:
                break
            for vocancy in vocancyes["items"]:
                salary = vocancy.get("salary")
                if salary and salary["currency"] == "RUR":
                    predict_salary = predict_rub_salary(vocancy["salary"].get("from"),vocancy["salary"].get("to"))
                    if predict_salary:
                        salary_vocancy.append(predict_salary)
        everage_salary = None
        if salary_vocancy:
            everage_salary = int(sum(salary_vocancy)/len(salary_vocancy)) 
            
        found_vocancy[lang] = {
            "vacancies_found": vocancyes["found"],
            "vacancies_processed": len(salary_vocancy),
            "average_salary": everage_salary,
        }
    return found_vocancy


def vocancy_sj(lang, page=0):
    sj_key = os.environ["SJ_KEY"]
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

    
def predict_rub_salary_for_superJob():
    found_vocancy = {}
    langs = [
    "python","java","javascript","ruby","php","c++","c#","C",
   ]
    for lang in langs:
        salary_vocancy=[]
        for page in count(0,1):
            vocancyes = vocancy_sj(lang, page=page)
            if page in vocancyes['objects']:
                break
            for vocancy in vocancyes["objects"]:
                predict_salary = predict_rub_salary(vocancy["payment_from"],vocancy["payment_to"])
                if predict_salary:
                    salary_vocancy.append(predict_salary)
        everage_salary = None
        if salary_vocancy:
            everage_salary = int(sum(salary_vocancy)/len(salary_vocancy)) 
            
        found_vocancy[lang] = {
            "vacancies_found": vocancyes["found"],
            "vacancies_processed": len(salary_vocancy),
            "average_salary": everage_salary,
        }
    return found_vocancy


def  table(title,statistics):
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    for lang, vocancyes in statistics.items():
        table_data.append([lang,vocancyes["vacancies_found"],vocancyes["vacancies_processed"],vocancyes["average_salary"]])
    table = AsciiTable(table_data, title)
    return table.table


def main():
    load_dotenv()
    print(table("hh Moscow",get_statistic_hh()))
    print(table("sj Moscow",vocancy_sj()))
    
    
if __name__ == "__main__":
    main()
    