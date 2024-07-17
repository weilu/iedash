# iedash
A Dash/Flask app for impact evaluation project tracking

## Development

First `git clone` this repo.

Then generate and obtain your access token from databricks following this instruction: https://docs.databricks.com/en/dev-tools/auth/pat.html
Get connection details for the SQL Warehouse compute resource which is used for providing the database connection: https://docs.databricks.com/en/integrations/compute-details.html

Export the obtained information to the following environment variables:

```bash
export ACCESS_TOKEN="[access token]"
export SERVER_HOSTNAME="[server hostname, e.g. adb-12345678.12.azuredatabricks.net"
export HTTP_PATH="[http path, e.g. /sql/1.0/warehouses/abcdxxx123]"
```


Then to setup and verify the app works locally:

```bash
pip install -r requirements.txt
flask db migrate
python app.py
open http://127.0.0.1:8050/
```
You should see the data app.

### Creating a test user

This app has simple authentication setup for demo purposes.
To view the pages behind the login screen, you will need to create a test user in the DB.
First, start the flask shell
```bash
flask shell
```

Then paste and execute the following code:

```py
from models import User, db
new_user = User(username='admin')
new_user.set_password('admin')
db.session.add(new_user)
db.session.commit()
```

You should then be able to login with username admin and password admin.

## Deployment

- Internal Server: https://w0lxdrconn01.worldbank.org
- External Server: https://w0lxdshyprd1c01.worldbank.org

Ensure you have an RStudio Connect account, if not [request here](https://worldbankgroup.service-now.com/wbg?id=ticket&table=sc_req_item&sys_id=fbb93028476502d09169d03fe16d4309). Upon account provisioning, generate API key(s) on the target server's UI.

Check which python version is supported by the server with:

```bash
rsconnect content search --server [server URL] --api-key [your API key] | jq -c '.[] | {}' | sort | uniq
```

As of writing both the internal and external server supports 3.8.14 so that's the version we are going to use for building & deploying the dash app. If you are using `pyenv` this repo's python version has configured to use 3.8.14. If the target server uses a different version, feel free to switch using `pyenv local 3.x.x`.


To deploy:

```bash
rsconnect deploy dash --server [server URL] --api-key [your API key] ./
```

