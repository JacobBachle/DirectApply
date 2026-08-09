from pathlib import Path
import sys

from directapply import storage

from common.commonPaths_DB import DB_DIRECTORY,DB_GENERATED_DIRECTORY,DB_SEARCH_CRITERIA_DIRECTORY
from common.commonPaths_DB import DB_SEARCH_CRITERIA_PATH,DB_JOB_LISTING_PATH

testDir = [DB_DIRECTORY,DB_GENERATED_DIRECTORY,DB_SEARCH_CRITERIA_DIRECTORY,
           DB_SEARCH_CRITERIA_PATH,DB_JOB_LISTING_PATH
           ]

for dir in testDir:
    storage.printPath_DB(dir)