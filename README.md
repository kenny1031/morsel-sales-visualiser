# Pink Morsel Sales Visualiser
A single‑page **Dash** application that ingests three daily‑sales CSV files, aggregates them into a tidy dataset, and lets you explore Pink Morsel revenue by region.  A slim Pytest suite and GitHub Actions workflow keep the UI working as the code evolves.

## Features
**Interactive dashboard** - Line‑chart built with Plotly; radio‑button filter to focus on any region or all at once.

**Price‑rise checkpoint** - Automatic before/after sales comparison for the 15 Jan 2021 price change.

**UI** - Buttons to display data for each region.

**Test suite** - Three Selenium‑powered tests (header / graph / region picker) via `dash[testing]`.

**CI‑ready** - `run_tests.sh` helper.
## Quickstart
```{bash}
# 1 Clone & enter repo
$ git clone https://github.com/<you>/pink-morsel-dashboard.git
$ cd pink-morsel-dashboard

# 2 Create venv & install deps
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

# 3 Run the app
$ python app.py
# visit http://127.0.0.1:8050 in your browser
```
## Running Tests
```{bash}
./run_tests.sh        # activates venv + pytest, exits 0/1
# or simply
pytest -q
```
The suite uses **webdriver‑manager** to pull the right ChromeDriver automatically, so it works locally and on CI runners with no extra setup.
## Project structure
```{bash}
.
├── app.py                     # Dash app
├── combine_data.py            # CSV merge helper
├── pink_morsel_sales.csv      # pre‑processed dataset
├── tests/
│   └── test_app.py            # Selenium tests
├── run_tests.sh               # local + CI test launcher
└── requirements.txt           # runtime + dev deps
```

## Requirements
* Python >= 3.9
* dash >= 2.16.1
* plotly >= 5.18
* pandas >= 2.2
* pytest >= 8.0, `dash[testing]`, webdriver-manager (dev only)

See `requirements.txt` for exact versions.
