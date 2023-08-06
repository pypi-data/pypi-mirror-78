import time
import sys
import logging
import vertica_python

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.captureWarnings(True)


class VerticaConnector:
    def __init__(
        self,
        user,
        password,
        database,
        vertica_configs,
        debug=True,
        sec_to_recconect=5,
        count_retries=1,
    ):

        """ pass params to connector
        :param user user in connection info
        :type  str
        :param password password in connection info
        :type slack_conn_id: str
        :param database
        :type str
        :param vertica_configs - other  required params including host, port, connection_load_balance, backup_server_node
        :param sec_to_recconect: seconds to reconnect
        :param count_retries
        """
        self.sec_to_recconect = 5
        self.count_retries = count_retries
        self.connection_info = vertica_configs
        self.connection_info["user"] = user
        self.connection_info["connection_load_balance"] = True
        self.connection_info["password"] = password
        self.connection_info["database"] = database
        self.debug = debug
        if "backup_server_node" not in self.connection_info:
            raise BaseException(
                "Error. You should specify backup_server_node list in connection_info"
            )
        elif len(self.connection_info["backup_server_node"]) == 0:
            raise BaseException(
                "Error. backup_server_node list has to contain at least one backup node"
            )
        if (
            "connection_load_balance" not in self.connection_info
            or not self.connection_info["connection_load_balance"]
        ):
            raise BaseException(
                "Error. You have to specify connection_load_balance=True param"
            )
        for param in ["host", "port", "user", "password", "database"]:
            if param not in self.connection_info:
                raise BaseException("Error. You have to specify {} param".format(param))

    def __str__(self):
        return "VerticaConnector to {}".format(self.connection_info["database"])

    def __enter__(self):
        """ start point to connect """
        if self.debug:
            logging.info("Connecting to Vertica...")
        for i in range(self.count_retries + 1):
            try:
                self.cnx = vertica_python.connect(**self.connection_info)
                break;
            except vertica_python.errors.ConnectionError as E:
                logging.info(
                    "{}, waiting {} sec to reconnect".format(
                        str(E), self.sec_to_recconect
                    )
                )
                time.sleep(self.sec_to_recconect)

        if self.debug:
            cur = self.cnx.cursor("dict")
            sql_sessions = """SELECT node_name, client_hostname, session_id, login_timestamp, transaction_id, client_version FROM CURRENT_SESSION"""
            cur.execute(sql_sessions)
            row = cur.fetchone()
            params = []
            for key, value in row.items():
                params.append(str(key) + ": " + str(value))

            logging.info(
                "Connected to Vertica: {current_session_info}".format(
                    current_session_info=", ".join(params)
                )
            )
        return self.cnx

    def __exit__(self, type, value, traceback):
        self.cnx.close()
        if self.debug:
            logging.info("Vertica connection closed")
