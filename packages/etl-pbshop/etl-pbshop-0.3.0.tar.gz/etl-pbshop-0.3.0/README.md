# ETL Lib

[![Upload Python Package](https://github.com/inovacaodigital/etl_pbshop_lib/workflows/Upload%20Python%20Package/badge.svg)](https://github.com/inovacaodigital/etl_pbshop_lib/workflows/Upload%20Python%20Package/badge.svg)
[![PyPI version](https://badge.fury.io/py/etl-pbshop.svg)](https://badge.fury.io/py/etl-pbshop)

This is a simple package built for Portobello Shop integrations, and now is available as ETL lib.
 
 Can be used with several services, like:
 * Oracle
 * Salesforce 
 * MSSQL Server
 * GSuite
 * Microvix
 * ODBC Drivers: PYODBC and SQLALCHEMY
 * And any REST services ...
 
 Comming soon:
 * RabbitMQ
 * Kafka
 * OpenVault (Credentials)
 * ...
 
 # Basic Usage 
 ## Rewrite ETL ABC class
 Use inheritance and rewrite the three abstract methods (even if you don't use it):
 
 ```python
from etl_pbshop import ETL, Connectors

class MyETL(ETL):
    def __init__(self):
        self.config = MyConfiguration()
        self.log = self.config.log
        self.connector = Connectors(
            config=self.config, 
            log=self.log, 
            services={'google': 'PROD', "salesforce": "PROD"}
        )

    def extract(self):
        pass  # extract the needed data using Connectors

    def transform(self): 
        pass  # do some transformations

    def load(self):
        pass  # upload your transformations
```

## Main caller:
On the main caller, you can simply:

 ```python
if __name__ == '__main__':
    etl = MyETL()
    etl.config.start()
    try:
        etl.run()
        exit(0)
    except Exception as e:
        etl.get_error(f"ERROR on main: {str(e)}")
        raise e
    finally:
        etl.config.finish()
```

## Rewriting default ConfigModel:
In another class, you can rewrite the ConfigModel class and input your values: 
 ```python
from etl_pbshop.config_model import ConfigModel

class MyConfiguration(ConfigModel):
    def __init__(self):
        super().__init__(__file__)
        self.SQL_QUERIES = {
            "produtos": "SELECT * FROM Products2"
        }
        self.INTEGRATION_SPREADSHEET_ID = '654asd5as1das5d165a4d68'     
```

## Environment variables:

You can put your environment variables to use the Connectors class.
In a `.env` file, set it in groups, like:

```.env
INTEGRACAO_ORACLE_ID_1=1
INTEGRACAO_ORACLE_TOKEN_VALUE_1=asd1234asd==
INTEGRACAO_ORACLE_TOKEN_URL_1=http://example.com/token
INTEGRACAO_ORACLE_METHOD_URL_1=http://example.com/method_to_post
INTEGRACAO_ORACLE_USER_1=asd..
INTEGRACAO_ORACLE_PASS_1=qwerty..
INTEGRACAO_ORACLE_ENVIRONMENT_1=DEV

INTEGRACAO_MICROVIX_ID_1=1
INTEGRACAO_MICROVIX_TOKEN_VALUE_1=1234-123-123-1234
INTEGRACAO_MICROVIX_METHOD_URL_1=https://webapi.microvix.com.br/1.0/api/method
INTEGRACAO_MICROVIX_USER_1=user
INTEGRACAO_MICROVIX_PASS_1=pass
INTEGRACAO_MICROVIX_ENVIRONMENT_1=PROD

INTEGRACAO_SALESFORCE_ID_1=1
INTEGRACAO_SALESFORCE_TOKEN_VALUE_1=qwerty
INTEGRACAO_SALESFORCE_METHOD_URL_1=https://login.salesforce.com/services/Soap/u/47.0
INTEGRACAO_SALESFORCE_USER_1=username@example.com
INTEGRACAO_SALESFORCE_PASS_1=myPass
INTEGRACAO_SALESFORCE_ENVIRONMENT_1=PROD
```

You only need to keep the pattern: `INTEGRACAO_<service_name>_<key_name>_<group_id>`

More info, please contact: [daniel.camargo@portobelloshop.com.br](mailto:daniel.camargo@portobelloshop.com.br)

