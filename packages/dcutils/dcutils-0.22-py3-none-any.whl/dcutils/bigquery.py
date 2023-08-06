import datetime
import logging
from requests.utils import quote
from google.cloud import bigquery as bq
from google.api_core.exceptions import NotFound

def create_table(client, datasetId, name, schema):
    # clean datasetId
    datasetId = quote(datasetId, safe='')

    # initialize logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    filehandler = logging.FileHandler('process_{}.log'.format(datetime.datetime.now()))
    filehandler.setLevel(logging.INFO)

    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.addHandler(filehandler)
    
    # initialize dataset and table reference
    ds_ref = client.dataset(datasetId)
    tb_ref = ds_ref.table(name)
    
    # create table if it does not exist
    try:
        client.get_table(tb_ref)
    except NotFound:
        table = bq.Table(tb_ref, schema=schema)
        table = client.create_table(table)
        logger.info('{}: CREATED TABLE {}'.format(datetime.datetime.now(), name))
        print('{}: CREATED TABLE {}'.format(datetime.datetime.now(), name))
