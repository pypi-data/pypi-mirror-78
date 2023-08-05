import pymongo
from sshtunnel import SSHTunnelForwarder
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

class CollectionCloner:
    def __init__(self, config):

        self.config = config
        
        self.mode = self.config.get('mode')

        self.src_db_name = self.config.get('src_db_name', '')
        self.src_col = self.config.get('src_col', '')
        self.src_db = self.config.get('src_db', '')
        self.src_ip = self.config.get('src_ip', '')
        self.des_db_name = self.config.get('des_db_name', '')
        self.user = self.config.get('user', '')
        self.password = self.config.get('password', '')
        self.des_col = self.config.get('des_col', '')
        self.des_ip = self.config.get('des_ip', '')
        
        if self.mode == 'll':
            self.clone_local_to_local()
        elif self.mode == 'lr':
            self.clone_local_to_remote()
        elif self.mode == 'rl':
            self.clone_remote_to_local()
        elif self.mode == 'rr':
            self.clone_remote_to_remote()
        else:
            logger.error('Allowed modes: ll, lr, rl, and rr')

        
    def clone_local_to_local(self):
        # Source

        if self.src_db_name == '':
            logger.error('No src_db_name is found')
        if self.src_col == '':
            logger.error('No src_col is found')
        if self.des_db_name == '':
            logger.error('No des_db_name is found')
        if self.des_col == '':
            logger.error('No des_col is found')
        
        try:
            src_client = pymongo.MongoClient('localhost')
        except Exception as e:
            logger.error('Could not connect to source local host')

        try:
            src_db = src_client[self.src_db_name]
        except Exception as e:
            logger.error('Could not find a database the with name: {}'.format(self.src_db_name))

        # Destinatoion 
        if self.des_db_name == '':
            logger.error('No des_db_name is found')
        if self.des_col == '':
            logger.error('No des_col is found')

        try:
            des_client = pymongo.MongoClient('localhost')
        except Exception as e:
            logger.error('Could not connect to destination local host')

        des_db = des_client[self.des_db_name]
        
        self.start_cloning(src_db, des_db)
    
    def clone_local_to_remote(self):
        if self.src_db_name == '':
            logger.error('No src_db_name is found')
        if self.src_col == '':
            logger.error('No src_col is found')

        try:
            src_client = pymongo.MongoClient('localhost')
        except Exception as e:
            logger.error('Could not connect to local host')

        try:
            src_db = src_client[src_db_name]
        except Exception as e:
            logger.error('Could not find a database the with name: {}'.format(self.src_db_name))

        # Destinatoion 
        if self.des_db_name == '':
            logger.error('No des_db_name is found')
        if self.user == '':
            logger.error('No user is found')
        if self.password == '':
            logger.error('No password is found')
        if self.des_col == '':
            logger.error('No des_col is found')
        if self.des_ip == '':
            logger.error('No des_ip is found')

        try:
            des_server = SSHTunnelForwarder(
                des_ip,
                ssh_username=self.user,
                ssh_password=self.password,
                remote_bind_address=('127.0.0.1', 27017)
            )
            des_server.start()
            des_client = pymongo.MongoClient('127.0.0.1', des_server.local_bind_port)
        except Exception as e:
            logger.error('Could not connect to destination remote server')
        
        des_db = des_client[self.des_db_name]
        
        self.start_cloning(src_db, des_db)
        
    def clone_remote_to_local(self):
        if self.src_db_name == '':
            logger.error('No src_db_name is found')
        if self.user == '':
            logger.error('No src_user is found')
        if self.password == '':
            logger.error('No src_pass is found')
        if self.src_col == '':
            logger.error('No src_col is found')
        if self.src_ip == '':
            logger.error('No src_ip is found')
        try:
            src_server = SSHTunnelForwarder(
                src_ip,
                ssh_username=self.user,
                ssh_password=self.password,
                remote_bind_address=('127.0.0.1', 27017)
            )
            src_server.start()
            src_client = pymongo.MongoClient('127.0.0.1', src_server.local_bind_port)
        except Exception as e:
            logger.error("Could not connect to source remote server")

        try:
            src_db = src_client[self.src_db_name]
        except Exception as e:
            logger.error('Could not find a database the with name: {}'.format(self.src_db_name))

        # Destinatoion 
        if des_db_name == '':
            logger.error('No des_db_name is found')
        if des_col == '':
            logger.error('No des_col is found')

        des_client = pymongo.MongoClient('localhost')
        des_db = des_client[self.des_db_name]
        
        self.start_cloning(src_db, des_db)
        
    def clone_remote_to_remote(self):
        if self.src_db_name == '':
            logger.error('No src_db_name is found')
        if self.user == '':
            logger.error('No user is found')
        if self.password == '':
            logger.error('No password is found')
        if self.src_col == '':
            logger.error('No src_col is found')
        if self.src_ip == '':
            logger.error('No src_ip is found')

        try:
            src_server = SSHTunnelForwarder(
                self.src_ip,
                ssh_username=self.user,
                ssh_password=self.password,
                remote_bind_address=('127.0.0.1', 27017)
            )

            src_server.start()
            src_client = pymongo.MongoClient('127.0.0.1', src_server.local_bind_port)
        except Exception as e:
            logger.error("Could not connect to source remote server")

        try:
            src_db = src_client[self.src_db_name]
        except Exception as e:
            logger.error('Could not find a database the with name: {}'.format(self.src_db_name))

        # Destinatoion 
        if self.des_db_name == '':
            logger.error('No des_db_name is found')
        if self.user == '':
            logger.error('No user is found')
        if self.password == '':
            logger.error('No password is found')
        if self.des_col == '':
            logger.error('No des_col is found')
        if self.des_ip == '':
            logger.error('No des_ip is found')

        try:
            des_server = SSHTunnelForwarder(
                self.des_ip,
                ssh_username=self.user,
                ssh_password=self.password,
                remote_bind_address=('127.0.0.1', 27017)
            )

            des_server.start()
            des_client = pymongo.MongoClient('127.0.0.1', des_server.local_bind_port)
        except Exception as e:
            logger.error('Could not connect to destination remote server')

        des_db = des_client[self.des_db_name]
        
        self.start_cloning(src_db, des_db)

    # Cloning database
    def start_cloning(self, src_db, des_db):
        for doc in src_db[self.src_col].find():
            try:
                des_db[self.des_col].insert(doc)
            except Exception as e:
                logger.debug('Could not insert document into destination collection')