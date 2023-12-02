import csv

from flask import Flask, request, render_template, Response
# from manual_db import handle_product, handle_district
from automation import auto_handle
from manual_db import handle_product
import io

app = Flask(__name__)

#index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html', a=1)
    else:
        return render_template('index.html')

#statistic page
@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    if request.method == 'POST':
        return render_template('statistic.html', b=1)
    else:
        return render_template('statistic.html')

#Admin page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        return render_template('admin.html', c=1)
    else:
        return render_template('admin.html')

# #GET product by District from Date range
# @app.route('/get-product/<product_id>/<district_id>/<from_date>/<to_date>')
# def get_data_product(product_id=None, district_id=None, from_date=None, to_date=None):
#   return handle_product.get_data(product_id, district_id, from_date, to_date)
#
# #GET product by District from Date range
# @app.route('/get-product-file/<product_id>/<district_id>/<from_date>/<to_date>')
# def get_data_product_file(product_id=None, district_id=None, from_date=None, to_date=None):
#   return handle_product.get_data_file(product_id, district_id, from_date, to_date)
#
# #GET product of 24 districts by Date
# @app.route('/get-product/all-dist/<product_id>/<date>')
# def get_data_product_all_dist(product_id=None,date=None):
#     return handle_product.get_data_all_dist(product_id, date)
#
#GET temperature by date
@app.route('/get-temperature/all-provinces/<date>')
def get_temperature_data_predict_all_Provinces(date=None):
    return handle_product.get_data_all_provinces(date)

#GET temperature by province_id and date
@app.route('/get-temperature/<province_id>/<start_date>/<end_date>')
def get_temperature_data(province_id=None, start_date=None, end_date=None):
    return handle_product.get_data_by_provinceId(province_id, start_date, end_date)

@app.route('/export-temperature/<province_id>/<start_date>/<end_date>')
def export_temperature_data(province_id=None, start_date=None, end_date=None):
    csv_blob = handle_product.export_province_data_to_csv(province_id, start_date, end_date)
    return Response(csv_blob, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=data.csv"})

# #add provinces to Database
@app.route('/add-province-to-db')
def addProvinceToDB():
  return auto_handle.addProvincesToDB()
#
# #add data to Database
@app.route('/add-data-to-db')
def addDataToDB():
  return auto_handle.addDataToDB()
#
#predict value and store to db
@app.route('/add-data-predict-to-db')
def addDataPredictToDB():
  return auto_handle.addDataPredictToDB()
#
# # calling sentinelCollectDataset function

if __name__ == "__main__":
    app.run("0.0.0.0", port=5500, debug=True)






