rm -rf pytest-results
pytest -n 5 --alluredir pytest-results
allure serve pytest-results