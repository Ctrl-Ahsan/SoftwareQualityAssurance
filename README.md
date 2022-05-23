```
 CISC327

Frontend, backend and security testing for a simple marketplace built using Flask and SQLAlchemy. Concepts applied:

- Git
- Docker
- Black / White Box Testing
- Systematic Testing
- Testing Automation
- Buffer Overflow, SQL Injection, XSS Prevention
```
[![Pytest-All](https://github.com/wilsonhammell/CISC327/actions/workflows/pytest.yml/badge.svg)](https://github.com/wilsonhammell/CISC327/actions/workflows/pytest.yml)
[![Python PEP8](https://github.com/wilsonhammell/CISC327/actions/workflows/style_check.yml/badge.svg)](https://github.com/wilsonhammell/CISC327/actions/workflows/style_check.yml)

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
│   │   ├── test_buy_prod.py     ======> Frontend tests for A6
│   │   ├── test_create_prod.py  ======> Tests for create product (R4-1 to R4-8)
│   │   ├── test_login.py        ======> Tests for login (R2-1 to R2-2)
│   │   ├── test_register.py     ======> Tests for register (R1-1 to R1-10)
│   │   ├── test_update_user.py  ======> Tests for updating user (R3-1 to R3-4)
│   │   └── test_update_prod.py  ======> Tests for update product (R5-1 to R5-4)
│   ├── __init__.py      ======> Required for a python module (can be empty)
│   ├── conftest.py      ======> Code to run before/after all the testing
│   └── test_models.py   ======> Testing code for models.py & A6 backend
├── A0-contract.md       ======> A0 contract
├── Screenshot 1.png     ======> Screenshot 1 for A4
├── Screenshot 2.png     ======> Screenshot 1 for A4
├── progress.md          ======> Progress update for A4
├── Dockerfile           ======> Defines what's included in container
├── SQL-Injection Chart.docx ======> SQL-Injection results chart
├── SQL-Injection Security Report.txt ======> Answers to SQL questions
├── a5-board.png         ======> A5 Project Board (Shows everyone's roles)
├── a5-progress-update.md ======> Progress updates from each member (A5 only)
├── a6-board.png         ======> A6 Project Board (Shows everyone's roles)
├── a6-progress-update.md ======> Progress updates from each member (A6 only)
├── db_init.sql          ======> Init database
├── docker-compose.yml   ======> Docker compose yml
├── XSS Scanner Security Report.txt ======> Answers to XSS questions
├── XSS Security Scan Chart.docx ======> XSS results chart
├── wait-for-it.sh       ======> Check available ports
└── requirements.txt     ======> Dependencies
```
