Customized vertica connector 
==========

The Python Wrapper to vertica_python lib for reconnectiong across server nodes


Usage
```sh
pip3 install vertica-connector-talenttech
```

```python
import os
import json
from vconnector.vertica_connector import VerticaConnector

user = "test_user",
password = "test_password"
database = "test_database"
vertica_configs = json.loads(os.getenv("VERTICA_CONFIGS"))


with VerticaConnector(user=user, 
                      password=password, 
                      database=database, 
                      vertica_configs=vertica_configs) as cnx:
      cur = cnx.cursor()
      sql = "SELECT 1"
      cur.execute(sql)
```

VERTICA_CONFIGS var structure
-------------
```sh
{"host": <VERTICA_HOST>,
 "port": <VERTICA_PORT>,
 "backup_server_node": [<SERVER_NODE_1>, <SERVER_NODE_2>, <SERVER_NODE_3>}
```
