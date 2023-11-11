from flask import Flask, escape, request
from handle_no2 import find_no2

app = Flask(__name__)

@app.route('/get-no2/')
def get_no2():
    res = find_no2(10.769900246474144, 106.67528565991044)
    return f'{res}'

if __name__ == "__main__":
    app.run("0.0.0.0", port=5600)   