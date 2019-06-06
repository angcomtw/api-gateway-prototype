# -*- coding: utf-8 -*-

import datetime
import logging
# import urllib.parse
from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource, reqparse
from sklearn.externals import joblib
from flask_cors import CORS
from flask_cache import Cache
import pgsqlhelper

cache = Cache()
app = Flask(__name__)
CORS(app, resources=r'/*')  # 跨域資源共享
app.config['JSON_AS_ASCII'] = False  # 如此便可處理中文
api = Api(app)  # 用API來綁定APP

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    filename='query_log.log',
                    filemode='w',
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )

# 註冊 Cache instance
cache = Cache(app, config={'CACHE_TYPE': 'redis',          # Use Redis
                           'CACHE_REDIS_HOST': 'localhost',  # Host, default 'localhost'
                           'CACHE_REDIS_PORT': 6379,       # Port, default 6379
                           'CACHE_REDIS_PASSWORD': '',  # Password
                           'CACHE_REDIS_DB': 2})           # DB, default 0
cache.init_app(app)  # cache初始化


class TestAPI(Resource):
    # @app.route('/testmodel/v1.0/loan<id>')
    # @cache.cached(timeout=5, key_prefix='cache_key')  # cache this view for 5 minutes
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument('id', type=str, required=True, help='This id is not exist')
        super(TestAPI, self).__init__()

    @cache.cached(timeout=10, key_prefix='cache_key')  # cache this view for 10 seconds
    def get(self):
        now = datetime.datetime.now()
        args = self.reqparse.parse_args(strict=True)
        conn = pgsqlhelper.get_conn()
        df = pgsqlhelper.get_data_by_id(conn, args['id'])
        return_key = cache_key()
        print(return_key)
        conn.close()
        clf = joblib.load('/api/MLaaS_gatewayv1/filename.pkl')

        predit_X = [[df['age'].values[0],
                     df['education'].values[0],
                     df['annualincome'].values[0]]]
        result = clf.predict(predit_X)

        # print(request.path)
        # 要把nparray轉為list .tolist()
        return jsonify({'query_time': str(now), 'result': result.tolist()})
        # return render_template('index.html')

    @cache.cached(timeout=10, key_prefix='cache_key')  # cache this view for 10 seconds
    def post(self):
        now = datetime.datetime.now()
        args = self.reqparse.parse_args(strict=True)
        conn = pgsqlhelper.get_conn()
        df = pgsqlhelper.get_data_by_id(conn, args['id'])
        return_key = cache_key()
        print(return_key)
        conn.close()
        clf = joblib.load('/api/MLaaS_gatewayv1/filename.pkl')

        predit_X = [[df['age'].values[0],
                     df['education'].values[0],
                     df['annualincome'].values[0]]]
        result = clf.predict(predit_X)

        # print(request.path)
        # 要把nparray轉為list .tolist()
        return jsonify({'query_time': str(now), 'result': result.tolist()})


# http://127.0.0.1:5010/testmodel/v1.0/loan?id=A177754800
# 21627091.91695168
api.add_resource(TestAPI, '/testmodel/v1.0/loan', endpoint='/testmodel/v1.0/loan')


# @cache.cached(timeout=60)  # cache this view for 1 minutes
def cache_key():
    #if request.method == 'get':
        #args = request.args
        # key = request.path + '?' + urllib.parse.urlencode([
        #     (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
	# ])
	#logging.debug('The Cache Function Has Been Called With %s' % args)
    	#return args
    #elif request.method == "post":
	# args = request.form
    logging.debug('The Cache Function Has Been Called With %s' % request.form)
    	# return args
		


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
