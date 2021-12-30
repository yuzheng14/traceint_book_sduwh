from traceint import seat_reserve, seat_pickup, seat_cancel, credit_sign
from flask import Flask, request, jsonify, make_response
from concurrent.futures import ThreadPoolExecutor
from traceint.utils.request import verify_cookie

app = Flask(__name__)
# app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False
executor = ThreadPoolExecutor(max_workers=10)
mylog = open('history.log', mode = 'a', encoding='utf-8')

@app.route('/test', methods=["GET"])
def test():
    if request.method == 'GET':

        response = make_response(jsonify({'message': 'OK'}, 200))
        return response


@app.route('/preserve', methods=["GET", "POST"])
def preserve():
    try:
        if request.method == 'POST':
            floor = request.get_json()['floor']
            seat = request.get_json()['seat']
            cookie = request.get_json()['cookie']
        if request.method == 'GET':
            floor = int(request.args.get('floor'))
            seat = int(request.args.get('seat'))
            cookie = request.args.get('cookie')
        if not verify_cookie(cookie):
            response = make_response(jsonify({'message': 'cookie无效，检查cookie'.encode('utf-8')}, 200))
            return response
        else:
            executor.submit(seat_reserve, cookie, floor, seat)
            response = make_response(jsonify({'message': 'cookie有效，请注意半小时内本程序生效'}, 200))
            return response
    except Exception as e:
        response = make_response(jsonify({'message': str(e)}, 200))
        return response


@app.route('/pickup', methods=["GET", "POST"])
def pickup():
    try:
        if request.method == 'POST':
            cookie = request.get_json()['cookie']
        if request.method == 'GET':
            cookie = request.args.get('cookie')
        if not verify_cookie(cookie):
            response = make_response(jsonify({'message': 'cookie无效，检查cookie'}, 200))
            return response
        else:
            executor.submit(seat_pickup, cookie, 12, False, False)
            response = make_response(jsonify({'message': 'cookie有效，请注意半小时内本程序生效'}, 200))
            return response
    except Exception as e:
        response = make_response(jsonify({'message': str(e)}, 200))
        return response


@app.route('/cancel', methods=["GET", "POST"])
def cancel():
    try:
        if request.method == 'POST':
            cookie = request.get_json()['cookie']
        if request.method == 'GET':
            cookie = request.args.get('cookie')
        if not verify_cookie(cookie):
            response = make_response(jsonify({'message': 'cookie无效，检查cookie'}, 200))
            return response
        else:
            if not seat_cancel(cookie):
                response = make_response(jsonify({'message': '请注意:  退座失败，请检查状态'}, 200))
                return response
            else:
                response = make_response(jsonify({'message': '退座成功'}, 200))
                return response
    except Exception as e:
        response = make_response(jsonify({'message': str(e)}, 200))
        return response


@app.route('/credit_sign', methods=["GET", "POST"])
def sign():
    try:
        if request.method == 'POST':
            cookie = request.get_json()['cookie']
        if request.method == 'GET':
            cookie = request.args.get('cookie')
        if not verify_cookie(cookie):
            response = make_response(jsonify({'message': 'cookie无效，检查cookie'}, 200))
            return response
        else:
            if not credit_sign(cookie):
                response = make_response(jsonify({'message': '请注意:  签到失败，请检查状态'}, 200))
                return response
            else:
                response = make_response(jsonify({'message': '签到成功'}, 200))
                return response
    except Exception as e:
        response = make_response(jsonify({'message': str(e)}, 200))
        return response

if __name__ == "__main__":
    app.config['SERVER_NAME'] = 'mylifemeaning.cn:8000'

    app.run('0.0.0.0')
