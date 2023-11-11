from flask import Flask, request, render_template
from handle_no2 import find_no2
import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html', a=1)
    else:
        return render_template('index.html')

@app.route('/get-no2')
def get_no2():
    lat_input = request.args.get('lat')
    lon_input = request.args.get('lon')
    res = find_no2(lat_input, lon_input)
    return f'{res}'


# @app.route('/create/<first_name>/<last_name>')
# def create(first_name=None, last_name=None):
#   return 'Hello ' + first_name + ',' + last_name


# @app.route('/get-no2/<lat>/<lon>', methods=['GET'])
# def getNo2(lat=None, lon=None):
#     res = find_no2(lat, lon)
#     return f'{res}'


if __name__ == "__main__":
    # app.debug = True
    app.run("0.0.0.0", port=5500)
