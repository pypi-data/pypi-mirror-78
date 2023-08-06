from google.cloud import storage
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def newly_uploaded_blobs(
    STORAGE_CLIENT,
    SRC_BUCKET,
    DEST_BUCKET,
    PARENT_FOLDER,
    depth 
):
    filehandler = logging.FileHandler('newly_uploaded.log')
    filehandler.setLevel(logging.INFO)

    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.addHandler(filehandler)
    logger.info('NEWLY UPLOADED BLOBS')
    logger.info('SOURCE BUCKET: {}'.format(SRC_BUCKET))
    logger.info('DEST_BUCKET: {}'.format(DEST_BUCKET))
    logger.info('TIMESTAMP: {}'.format(datetime.datetime.now()))
    
    current_blobs_itr = STORAGE_CLIENT.list_blobs(DEST_BUCKET)
    src_blobs = STORAGE_CLIENT.list_blobs(SRC_BUCKET)
    new_blobs = []
    current_blobs = []
    
    for blob in current_blobs_itr:
        current_blobs.append(blob.name)

    for blob in src_blobs:
        folders = blob.name.split('/')
        if PARENT_FOLDER in folders[depth]:
            if blob.name not in current_blobs:
                new_blobs.append(blob)
                logger.info('{}'.format(blob.name))
    if len(new_blobs) == 0:
        logger.info('{} is updated with respect to {}'.format(DEST_BUCKET, SRC_BUCKET))
    return new_blobs