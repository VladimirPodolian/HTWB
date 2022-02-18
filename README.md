# Home Tests from WiseBits
UI automation for the [SQL playground page](https://www.w3schools.com/sql/trysql.asp?filename=trysql_asc)

---

# Tests executing:

## Docker
Install and start [docker](https://www.docker.com/) in your computer.

Start automation by command `docker-compose run --rm tests pytest -vv tests/ --headless --alluredir=.venv/allure
`

Note: `--headless` arg required. `--alluredir` arg is optional.

## Local:

1. Install [Chromedriver](https://chromedriver.chromium.org/). It should be placed in `PATH` env variable.
For MacOS, `chromderiver` can be installed with `brew install chromedriver`

2. Need to create venv from project directory and activate him:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Start automation by command `pytest -vv tests/ --alluredir=.venv/allure`. 

Note: `--headless` and `--alluredir` args are optional.

---

# Allure report:
Allure report can be generated after `local` or `docker` automation by `allure serve .venv/allure`
