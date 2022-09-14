from mongoengine import connect


class MongoDB:
    host = '127.0.0.1'
    port = 27017
    authentication_source = ''
    dbname = 'traffic'
    dbname2 = 'userInfo'
    alias = 'traffic'
    alias2 = 'userInfo'

    host_remote = '166.111.7.106'
    port_remote = 30020
    user = 'xll'
    dbname_remote = 'NePtune'
    passwd = 'xllKEG2022'
    alias_remote = 'NePtune'

    @classmethod
    def connect(cls):
        # for local connection
        connect(db=cls.dbname, host=cls.host, port=cls.port, authentication_source="traffic", alias=cls.alias)
        connect(db=cls.dbname2, host=cls.host, port=cls.port, authentication_source="'userInfo'", alias=cls.alias2)
        # for remote connection
        connect(db=cls.dbname_remote, host=cls.host_remote, port=cls.port_remote, username=cls.user,
                password=cls.passwd, authentication_source="NePtune", alias=cls.alias_remote)
