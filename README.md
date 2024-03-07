# mars-air
This project demonstrates test automation using both Python's unittest and pytest frameworks. We prefer pytest over unittest as it has lesser boilerplate code and an extensive plugin ecosystem, such as pytest-xdist, which enables parallel test execution and speeds up overall execution time.

Additionally, we prefer automating API over UI as the former is faster and less prone to brittleness compared to UI testing. We may prioritise UI testing over API is we need to validate things that API testing is not able to do so, such as CSS rendering and navigating from one page to another, with or without url change.

## Setup
### Virtual Environment
Virtualenv is a tool used for creating isolated Python environments. Below are the installation steps:
1. Git clone this repo onto your local machine.
2. Run the following command in the repo's root directory to create the virtual environment.
**Note**: ```pip install virtualenv``` if ```pip freeze|grep virtualenv``` returns empty.
    ```sh
    # For Python 2
    python2 -m virtualenv .venv
    
    # For Python 3
    python3 -m venv .venv
    ```
3. Run the following command in to activate the virtual environment. 
    ```sh
    # On macOS and Linux
    source .venv/bin/activate
    
    # On Windows
    .venv\Scripts\activate
    ```
4. Install project dependencies via requirements.txt.
    ```sh
    # For Python 2
    pip install -r requirements.txt
    
    # For Python 3
    pip3 install -r requirements.txt
    ```
5. [Optional] Configure your IDE's Python interpreter
   You may refer to [Pycharm](https://code.visualstudio.com/docs/python/environments) or [VS Code](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) for the installation steps.
### Playwright
Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API. You may refer to [Installing Playwright Pytest](https://playwright.dev/python/docs/intro) for installation steps.
### Allure Report
Allure Report is the utility that processes test results collected by a compatible test framework and produces an HTML report. You may refer to [Allure Report installation](https://allurereport.org/docs/gettingstarted-installation/) for installation steps.

## Execute tests and Generate Allure Report
The provided bash scripts execute Python unittest and pytest, storing the results in test-result/unittest and test-result/pytest respectively. Additionally, the scripts generate and serve an Allure report based on the test results. You can refer to the sample reports for unittest and pytest in the allure-report/unittest and allure-report/pytest directories, respectively.
   ```sh
    # Python unittest
    sh run_unittest.sh
    
    # Python pytest
    sh run_pytest.sh
   ```
