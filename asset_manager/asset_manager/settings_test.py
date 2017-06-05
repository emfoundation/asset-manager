from asset_manager.settings_dev import *

# Overwrite S3 bucket and logs
AWS_STORAGE_BUCKET_NAME = AWS_TEST_BUCKET_NAME
LOGFILE='logs/logs_test.txt'
