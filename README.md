# apm-report
Simple tool for extracting a report of all APM applications in a New Relic account.

## Getting started

1. Clone the repository
2. CD into the repository directory
3. Create a Python 3 virtual environment, install dependencies, and activate it.

```
virtualenv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
```

4. Set the USER_API_KEY environment variable 

```
export USER_API_KEY=A_NEW_RELIC_USER_API_KEY
```

5. Run the program

```
python apm-report.py
```

6. Explore and analyze the output file `apm-report.csv`

7. Included fields...

```
'Tribe',
'Squad',
'squad',
'name',
'reporting',
'language',
'Environment',
'Application',
'Cost-Center',
'feature',
'Location',
'accountid',
'Service',
'trustedAccountId',
'feature',
'account',
'squad',
'Alerting',
'Contact',
'guid',
'accountId',
'permalink'
```
