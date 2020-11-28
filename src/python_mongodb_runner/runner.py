from .utils import get_open_port
from .exceptions import MongoServerError
from pathlib import Path
import shutil
import tempfile
import os
import subprocess
from typing import Optional

MONGOD_EXE = "MONGOD_EXECUTABLE"

class MongoRunner(object):
    def __init__(self, data_directory: Path = None, port: int = None):
        
        # Check the installation directory of MongoDB
        mongo_exec = os.getenv(MONGOD_EXE)

        if mongo_exec is None:
            raise MongoServerError(f"Mongo executable path is not set.  Please set {MONGOD_EXE} environment variable")

        self._mongo_exec = Path(mongo_exec)
        
        self._port = port or get_open_port()
        self._data_directory = data_directory or self._get_temp_data_directory()
        
        if not self._data_directory.exists():
            raise MongoServerError(f"Specified data directory {data_directory} does not exist")

        self.mongo_process: subprocess.Popen = None

    def _get_temp_data_directory(self) -> Path:
        temp_dir = tempfile.mkdtemp()
        return Path(temp_dir)

    def _get_uri(self) -> str:
        return f'mongodb://127.0.0.1:{self._port}/{self._data_directory.name}?'


    def _start_server(self):        
        # open subprocess
        self._mongo_process = subprocess.Popen([str(self._mongo_exec), '--dbpath', str(self._data_directory), '--port', str(self._port)])

    def stop(self):        
        if self._mongo_process and self._mongo_process.poll() is None:
            self._mongo_process.kill()        

    """ Gets the uri connection string to the running mongo instance"""
    def get_uri(self) -> str:
        # start the mongo server
        self._start_server()

        # return the connection string
        return self._get_uri()

    def close(self):
        self.stop()
        shutil.rmtree(self._data_directory)
    
    def __del__(self):
        self.close()
