import json
import datetime
import uuid
import re
import pandas as pd
from setup_database import *


def upload_local_items(col):
    with open('../data/data1.json', 'r') as f:
        content = json.load(f)
        col.insert_many_collections([content])



if __name__ == '__main__':
    col = Collection()
    upload_local_items(col)