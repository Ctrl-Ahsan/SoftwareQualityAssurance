# CISC327

[![Pytest-All](https://github.com/CISC-CMPE-327/Python-CI-2021/actions/workflows/pytest.yml/badge.svg)](https://github.com/CISC-CMPE-327/Python-CI-2021/actions/workflows/pytest.yml)
[![Python PEP8](https://github.com/CISC-CMPE-327/Python-CI-2021/actions/workflows/style_check.yml/badge.svg)](https://github.com/CISC-CMPE-327/Python-CI-2021/actions/workflows/style_check.yml)

```
├── LICENSE
├── README.md
├── .github
│   ├── workflows
│   │   ├── pytest.yml          ======> CI settings for running test automatically (trigger test for commits/pull-requests)
│   │   └── style_check.yml     ======> CI settings for checking PEP8 automatically (trigger test for commits/pull-requests)
│   └─ pull_request_template.md ======> PR template
├── qbay                 ======> Application source code
│   ├── templates        ======> HTML templates
│   │   ├── base.html    ======> Base template to inherit from
│   │   ├── create.html  ======> Template for create product
│   │   ├── index.html   ======> Template for the main page
│   │   ├── login.html   ======> Template for the login page
│   │   ├── profile.html ======> Template to update profile
│   │   ├── register.html======> Template to register
│   │   └─ update.html   ======> Template to update product
│   ├── __init__.py      ======> Required for a python module (can be empty)
│   ├── __main__.py      ======> Program entry point
│   ├── controllers.py   ======> Controllers for website
│   └── models.py        ======> Data models
├── qbay_test            ======> Testing code
│   ├── frontend         ======> Contains frontend tests
│   │   ├── test_create_prod.py  ======> Tests for create product
│   │   ├── test_login.py        ======> Tests for login
│   │   ├── test_register.py     ======> Tests for register
│   │   └── test_update_prod.py  ======> Tests for update product
│   ├── __init__.py      ======> Required for a python module (can be empty)
│   ├── conftest.py      ======> Code to run before/after all the testing
│   └── test_models.py   ======> Testing code for models.py
├── A0-contract.md       ======> A0 contract
├── Screenshot 1.png     ======> Screenshot 1 for A4
├── Screenshot 2.png     ======> Screenshot 1 for A4
├── progress.md          ======> Progress update for A4
└── requirements.txt     ======> Dependencies
```
