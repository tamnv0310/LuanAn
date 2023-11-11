from flask import Flask, request, render_template
# from db import handle_no2, handle_product, handle_district
from db import handle_product, handle_district

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

#GET product by District from Date range
@app.route('/get-product/<product_id>/<district_id>/<from_date>/<to_date>')
def get_data_product(product_id=None, district_id=None, from_date=None, to_date=None):
  return handle_product.get_data(product_id, district_id, from_date, to_date)

#GET product of 24 districts by Date
@app.route('/get-product/all-dist/<product_id>/<date>')
def get_data_product_all_dist(product_id=None,date=None):
    return handle_product.get_data_all_dist(product_id, date)
    
#GET product forecast of 24 districts by Date
@app.route('/get-product-forecast/all-dist/<product_id>/<date>')
def get_data_product_predict_all_dist(product_id=None,date=None):
    return handle_product.get_data_predict_all_dist(product_id, date)

#GET all 24 districts
@app.route('/get-district-all')
def get_district_all():
  return handle_district.get_all()

if __name__ == "__main__":
    app.run("0.0.0.0", port=5500, debug=True)
