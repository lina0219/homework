from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    fruit = request.form['fruit']
    name = request.form['name']
    num1 = request.form['num1']
    num2 = request.form['num2']
    num3 = request.form['num3']
    address = request.form['address']
    memo = request.form['memo']

    order = {'fruit': fruit, 'name': name, 'num1': num1, 'num2': num2, 'num3': num3, 'address': address, 'memo': memo}
    db.orders.insert_one(order)

    return jsonify({'result': 'success'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def read_orders():
    result = list(db.orders.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'orders': result})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)