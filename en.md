# Comparing programmer vacancies

The project was created to compare the salaries of programming languages on the site [hh.ru ](https://dev.hh.ru /) and [SuperJob](https://api.superjob.ru /).
### How to install
Download the necessary files, then use ``pip`' (or `pip3` if there is a conflict with Python2) to install the dependencies. Dependencies can also be set with the command below:



```
pip install requirements.txt
```

## Example of running a script
To run the script, you must already have Python3 installed.

To get information in the table, you need to write:

```
python main.py
```
## Environment variables
Most of the settings are taken from the environment variables. Environment variables are variables in which values are assigned to a Python program. To determine them, you need to create a file ``.env`` and write the data there in this format: VARIABLE=value.

Example of the content from the .env file:
```
SJ_KEY="SJ_TOKEN"
```
You can also get the ``SJ_TOKEN`` token on the [Superjob API] website(https://api.superjob.ru /)
### The purpose of the project

The code was written for educational purposes in an online course for web developers [dvmn.org ](https://dvmn.org /).