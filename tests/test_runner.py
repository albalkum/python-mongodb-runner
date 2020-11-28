from python_mongodb_runner import MongoRunner
import pytest
import pymongo


@pytest.fixture
def mock_mongod_exec(monkeypatch):
    monkeypatch.setenv("MONGOD_EXECUTABLE", r'/bin/mongod')


def test_uri(mock_mongod_exec):
    # Assemble
    runner = MongoRunner()

    # ACT
    uri = runner.get_uri()

    # ASSERT
    assert uri == f'mongodb://127.0.0.1:{runner._port}/{runner._data_directory.name}?'

def test_temp_directory_removed(mock_mongod_exec):
    # Assemble
    runner = MongoRunner()
    runner.get_uri()
    data_dir = runner._data_directory

    assert data_dir.exists()

    # ACT
    runner.close()

    # ASSERT
    assert not data_dir.exists()


def test_mongo_process_runs(mock_mongod_exec):
    # Assemble
    runner = MongoRunner()
    runner.get_uri()
    mongo_process = runner._mongo_process

    assert mongo_process.poll() is None

    # ACT
    runner.close()

    # ASSERT
    assert mongo_process.poll() is not None

def test_connect_to_mongodb(mock_mongod_exec):
    # Assemble
    runner = MongoRunner()
    uri = runner.get_uri()

    # ACT
    client = pymongo.MongoClient(uri)
    
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')

    # if we reached this line we're good!
    return