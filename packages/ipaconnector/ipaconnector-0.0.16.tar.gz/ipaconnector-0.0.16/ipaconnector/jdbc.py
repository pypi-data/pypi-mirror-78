import jaydebeapi

from ipaconnector.klass import LoggingClass, TranslatedObject


class JdbcDriver(LoggingClass):
    HIVE_DRIVER = "org.apache.hive.jdbc.HiveDriver"

    def __init__(self, host, principal, port=10000, db="default"):
        self.url = f"jdbc:hive2://{host}:{port}/{db};principal={principal};ssl=true"
        self.connection = None
        self.cursor = None

    def connect(self):
        if not self.connection:
            self.connection = jaydebeapi.connect(self.HIVE_DRIVER, self.url)
            self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def query(self, sql):
        self._log.debug(f"HIVE: {sql}")
        self.cursor.execute(sql)
        try:
            output = self.cursor.fetchall()
            self._log.debug(f"HIVE_output: {output}")
            return output
        except jaydebeapi.Error:
            self._log.info("Couldn't get output")

    def __enter__(self):
        if not self.connection:
            self.connect()
        if not self.cursor:
            self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        self.disconnect()


def _generate_uri(dbname: str):
    """
    turns:
    prv_tes_zi01_usr -> /data/prv_tes/zi01/usr
    dev_zi00_ -> /data/dev/zi00/*
    """
    _funcitons = ['adm', 'source', 'trv', 'socle', 'metier', 'extr']
    splitted_name = dbname.split("_")
    if len(splitted_name) < 4:
        first_part = splitted_name[0]
        tech_number = splitted_name[1]
        func = splitted_name[2]
    else:
        first_part = "_".join(splitted_name[:2])
        tech_number = splitted_name[2]
        func = splitted_name[3]
    if func != "*":
        return [(dbname, f"/data/{first_part}/{tech_number}/{func}")]
    return [("_".join([first_part, tech_number, _func]), f"/data/{first_part}/{tech_number}/{_func}")
            for _func in _funcitons]


class Hive(LoggingClass):
    def __init__(self, jdbc: JdbcDriver):
        self._jdbc = jdbc
        if not self._jdbc.connection:
            self._jdbc.connect()

    def show_databases(self):
        output = self._jdbc.query("show databases")
        return [db_name[0] for db_name in output]

    def show_role_grant_group(self, group):
        output = self._jdbc.query(f"SHOW ROLE GRANT GROUP `{group}`")
        return [grant[0] for grant in output]

    def show_grant_role(self, role):
        output = self._jdbc.query(f"SHOW GRANT ROLE `{role}`")
        return [grant[0] for grant in output]

    def create_database(self, dbname, uri, description="DB created automatically", drop_if_exists=True):
        if drop_if_exists:
            self._log.info("Drop DB if exists")
            self._jdbc.query(f"DROP DATABASE IF EXISTS {dbname} CASCADE")
        self._log.info(f"Creating DB {dbname} at {uri} with comment {description}")
        self._jdbc.query(f'CREATE DATABASE `{dbname}` COMMENT "{description}" LOCATION "{uri}"')

    def create_role(self, role_name):
        self._log.info(f"Creating role {role_name}")
        self._jdbc.query(f"CREATE ROLE `{role_name}`")

    def grant_access_to_db(self, db, uri, role, cluster, permissions="ALL"):
        permissions = permissions.upper()
        self._log.info(f"Grant {permissions} to DB {db} on {uri} to {role}")
        self._jdbc.query(f"GRANT {permissions} ON DATABASE `{db}` TO ROLE `{role}`")
        # Grant ALL on URI only if necessary
        if any(perm in ["ALL", "CREATE", "INSERT"] for perm in permissions.upper().split(',')):
            self._jdbc.query(f"GRANT ALL ON URI 'hdfs://{cluster}-ha{uri}' TO ROLE `{role}`")

    def add_group_to_role(self, group, role):
        self._log.info(f"Adding group {group} to {role}")
        self._jdbc.query(f"GRANT ROLE `{role}` TO GROUP `{group}`")

    def drop_old_role(self, role):
        self._log.info(f"DROP ROLE {role}")
        try:
            self._jdbc.query(f"DROP ROLE `{role}`")
        except jaydebeapi.DatabaseError:
            self._log.info(f"ROLE {role} doesn't exists")


class PrivateZone(LoggingClass, TranslatedObject):
    def __init__(self, input_data: dict):
        self._info = self._translate(input_data)
        self.tech_name = self._info.get("techName")
        self.cluster = self._info.get("primaryKey").get("cluster")
        self.description = self._info.get("description")
        self.rw_groups = self.get_rw_groups()
        self.ro_groups = self.get_ro_groups()

    def add_new_database(self, hive_interface: Hive):
        db_uri = _generate_uri(self.tech_name)
        for db_name, uri in db_uri:
            self._create_single_db(hive_interface, db_name, uri)

    def _create_single_db(self, hive_interface, db_name, uri):
        hive_interface.create_database(db_name, uri=uri, description=self.description)
        ro_role_name = f"user_access_r_{db_name}"
        rw_role_name = f"user_access_rw_{db_name}"
        hive_interface.drop_old_role(rw_role_name)
        hive_interface.drop_old_role(ro_role_name)
        if self.ro_groups:
            hive_interface.create_role(ro_role_name)
            for group in self.ro_groups:
                hive_interface.add_group_to_role(group, ro_role_name)
            hive_interface.grant_access_to_db(db_name, uri, ro_role_name, self.cluster, permissions="SELECT")

        if self.rw_groups:
            hive_interface.create_role(rw_role_name)
            for group in self.rw_groups:
                hive_interface.add_group_to_role(group, rw_role_name)
            hive_interface.grant_access_to_db(db_name, uri, rw_role_name, self.cluster)

    def _get_add_value(self, key_name: str):
        groups = self._info.get(key_name, None)
        if not groups:
            return []
        return groups['add']

    def get_rw_groups(self):
        rw_groups = []
        rw_groups.extend(self._get_add_value("userGroupsRW"))
        rw_groups.extend(self._get_add_value("appUserGroupsRW"))
        return rw_groups

    def get_ro_groups(self):
        ro_groups = []
        ro_groups.extend(self._get_add_value("userGroupsR"))
        ro_groups.extend(self._get_add_value("appUserGroupsR"))
        return ro_groups
