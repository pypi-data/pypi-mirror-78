from abc import ABC, abstractmethod
from types import SimpleNamespace

from ipaconnector.jdbc import JdbcDriver, Hive


_CLUSTERS = {
    "elara": "elara-edge-u2-n01.dev.mlb.jupiter.nbyt.fr",
    "leda": "leda-edge-u2-n01.dev.mlb.jupiter.nbyt.fr",
    "callisto": "callisto-edge-u2-n01.dev.mlb.jupiter.nbyt.fr",
    "ganymede": "ganymede-edge-u2-n01.dev.mlb.jupiter.nbyt.fr",
}


class CLUSTER:
    # HOST = ""
    # PRINCIPAL = ""
    # _JDBC = JdbcDriver(HOST, PRINCIPAL)

    @classmethod
    def get_hive_interface(cls):
        _JDBC = JdbcDriver(cls.HOST, cls.PRINCIPAL)
        return Hive(_JDBC)


class ELARA(CLUSTER):
    HOST = "elara-edge-u2-n01.dev.mlb.jupiter.nbyt.fr"
    PRINCIPAL = "hive/elara-edge-u2-n01.dev.mlb.jupiter.nbyt.fr@DEV.MLB.JUPITER.NBYT.FR"
    DOMAIN = "DEV.MLB.JUPITER.NBYT.FR"


class LEDA(CLUSTER):
    HOST = "elara-edge-u2-n01.dev.mlb.jupiter.nbyt.fr"
    PRINCIPAL = "hive/elara-edge-u2-n01.dev.mlb.jupiter.nbyt.fr@DEV.MLB.JUPITER.NBYT.FR"
    DOMAIN = "MLB.JUPITER.NBYT.FR"


class CALLISTO(CLUSTER):
    HOST = "callisto-edgeg-u2-n02.mlb.jupiter.nbyt.fr"
    PRINCIPAL = "hive/callisto-edgeg-u2-n02.mlb.jupiter.nbyt.fr@MLB.JUPITER.NBYT.FR"
    DOMAIN = "MLB.JUPITER.NBYT.FR"


class GANYMEDE(CLUSTER):
    HOST = "elara-edge-u2-n01.dev.mlb.jupiter.nbyt.fr"
    PRINCIPAL = "hive/elara-edge-u2-n01.dev.mlb.jupiter.nbyt.fr@DEV.MLB.JUPITER.NBYT.FR"
    DOMAIN = "MLB.JUPITER.NBYT.FR"
