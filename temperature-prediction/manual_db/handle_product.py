import csv

import pandas as pd
from pymongo import MongoClient, collection
import json
from bson import json_util
import datetime
import numpy as np

from os.path import dirname as dir
from sys import path
import pandas as pd
from pymongo import MongoClient, collection
import json
from bson import json_util
from datetime import datetime, timedelta
import io
import numpy as np


#Connect to Database Host
client = MongoClient("localhost:27017")
# Select the database and collection
db = client.temperature_predict
province_list = db.provinces
temperature_collection = db.temperature
#Get data by Product, District ID, Date range
# def get_data(product_id=None, district_id=None, from_date=None, to_date=None):
#


def get_data_all_provinces(dt=None):
    print("====Info get_data_all_dist", dt,pd.to_datetime(dt,format='%Y-%m-%d', errors='coerce'))
    # Define the start date (replace with the date you want to start from)
    date_format = '%d-%m-%Y'

    datetime_obj = datetime.strptime(dt, date_format)
    start_date = datetime_obj  # Example: 2023-11-12
    end_date = start_date + timedelta(days=1)  # Adding 1 days to the start date

    # Aggregation pipeline
    pipeline = [
        {
            "$match": {
                "date": start_date  # Query data exactly for the start_date
            }
        },
        {
            "$group": {
                "_id": "$date",  # Group by date
                "temperatures": {
                    "$push": {
                        "province": "$province_id",
                        "val": "$val"
                    }
                }
            }
        },
        {
            "$project": {
                "query_date": {
                    "$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$_id"}
                },
                "data": {
                    "$arrayToObject": {
                        "$map": {
                            "input": "$temperatures",
                            "as": "temp",
                            "in": {
                                "k": "$$temp.province",
                                "v": "$$temp.val"
                            }
                        }
                    }
                },
                "_id": 0
            }
        },
        {"$limit": 1}  # Limit the result to only 1 document
    ]

    # Execute the aggregation pipeline
    result = temperature_collection.aggregate(pipeline)
    response = []

    # Process and format the results
    for item in result:
        jsonItem = json.dumps(item, default=json_util.default, ensure_ascii=False)
        response.append(json.loads(jsonItem))  # Convert JSON string to dictionary

    print(response)
    return response[0] if response else None


#Get data forecast by Product, one Date
def get_data_predict_all_dist(product_id=None,dt=None):
    print("====Info get_data_predict_all_dist", dt,pd.to_datetime(dt,format='%Y-%m-%d', errors='coerce'))
    #get Collection
    coll_pred = db[product_id+"_forecast"]
    # coll_pred = db[product_id+'_forecast']
    coefficient = 1000000
    if product_id == "pm25":
        coefficient = 1
    return_data = {
        'query_date': dt,
        'product_id': product_id,
        'data': {}
    }

    #Query data:
    query_date = pd.to_datetime(dt,format='%Y-%m-%d', errors='coerce')
    for doc in coll_pred.find({'date': query_date}):
        print(doc['dist_id'])
        return_data['data'][doc['dist_id']] = doc['val_pred'] * coefficient

    return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)


def get_data_by_provinceId(province_id=None, start_date=None, end_date=None):

    date_format = '%Y-%m-%d'
    start_date_obj = datetime.strptime(start_date, date_format)
    end_date_obj = datetime.strptime(end_date, date_format)
    # Query to find documents
    query = {
        "province_id": province_id,
        "date": {
            "$gte": start_date_obj,
            "$lt": end_date_obj
        }
    }

    # Define the projection
    projection = {
        "val": 1,
        "isForecast": 1,
        "_id": 0  # Exclude the _id field
    }

    # Find the documents with the specified projection
    documents = temperature_collection.find(query, projection)

    # Convert documents to JSON
    json_result = json.dumps(list(documents), default=json_util.default)

    print(json_result)
    return json_result


def export_province_data_to_csv(province_id=None, start_date=None, end_date=None):
    date_format = '%Y-%m-%d'
    start_date_obj = datetime.strptime(start_date, date_format)
    end_date_obj = datetime.strptime(end_date, date_format)

    # Query to find documents
    query = {
        "province_id": province_id,
        "date": {
            "$gte": start_date_obj,
            "$lt": end_date_obj
        }
    }

    # Define the projection
    projection = {
        "province_id": 1,
        "date": 1,
        "val": 1,
        "isForecast": 1,
        "_id": 0  # Exclude the _id field
    }

    # Create a mapping of English to Vietnamese column headers
    column_mapping = {
        "province_id": "Location",
        "date": "Date",
        "val": "Value",
        "isForecast": "isForecast",
    }


    # Find the documents with the specified projection
    documents = temperature_collection.find(query, projection)

    # Convert documents to a list of dictionaries
    documents_list = list(documents)

    # Convert documents to a list of dictionaries and format the date field
    for doc in documents_list:
        doc["date"] = doc["date"].strftime("%d/%m/%Y")  # Format the date as "ngày tháng năm"

    # Create a buffer and write CSV data to it
    buffer = io.StringIO()
    fieldnames = ["Location", "Date", "Value", "isForecast"]  # Vietnamese column headers
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    # writer.writerows(documents_list)

    # Map the keys in data to the Vietnamese column headers and write the data
    for row in documents_list:
        mapped_row = {column_mapping[key]: value for key, value in row.items()}
        writer.writerow(mapped_row)

    # Get the CSV content as a string and then encode it to bytes
    csv_content = buffer.getvalue().encode('utf-8')

    # Close the buffer
    buffer.close()

    return csv_content