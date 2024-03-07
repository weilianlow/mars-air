rm -rf test-result/unittest
python -m unittest_runner
allure serve test-result/unittest