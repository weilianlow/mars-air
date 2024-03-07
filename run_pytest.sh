rm -rf test-result/pytest
pytest -n 5 --alluredir test-result/pytest
allure serve test-result/pytest