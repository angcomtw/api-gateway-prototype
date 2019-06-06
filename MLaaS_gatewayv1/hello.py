from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from sklearn.externals import joblib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Required
import datetime
import numpy as np
#import pandas as pd
from flask import Flask,jsonify,request
from flask import make_response
from flask_restful import Api,Resource,reqparse
import logging
import pgsqlhelper


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'secret string'
api = Api(app)

#configure logging
logging.basicConfig(level=logging.DEBUG,
		    filename='api_query_log.log',
		    filemode='w',
		    format=
		    '%(asctime)s - %(pathname)s[Line:%(lineno)d] - %(levelname)s: %(message)s'


)


@app.route('/')
def hello_index():
    #return render_template('index.html')
    response = make_response(render_template('index.html'))
    response.set_cookie('myjwt','eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjAwMDEifQ.eyJuYW1lIjoiUXVvdGF0aW9uIFN5c3RlbSIsInN1YiI6ImFsaWNlIiwiaXNzIjoiTXkgQVBJIEdhdGV3YXkifQ.qcfgTHuyE4BPTT9Rrqvqpa75NuAd7M6SrAGlphyuYiA',secure=True)
    return response

@app.route('/api_pool/api1',methods=['POST','GET'])
def view():
    query = None
    predict_value = None
    json_dict=dict()
    form = InputLabelForm() #check the input value cannot be empty value
    if form.validate_on_submit():
        logging.info("API is Started! The query is %s" % form.query_string.data)
        query = form.query_string.data
        form.query_string.data = ' ' 
        now = datetime.datetime.now()
        conn = pgsqlhelper.get_conn()
        df = pgsqlhelper.get_data_by_id(conn, query)
        print(df)
        conn.close()
    
        clf = joblib.load('/api/MLaaS_gatewayv1/filename.pkl')
        predict_X = [[df['age'].values[0],
                 df['education'].values[0],
                 df['annualincome'].values[0]]]
        print(predict_X)   
        result = clf.predict(predict_X)
        predict_value = str(result[0][0])
        print(predict_value)
        json_dict = {"query_time":now,
                     "result":predict_value}
        logging.info("Final predict value is %s" % predict_value)
        return jsonify(json_dict)
    #logging.info("Final predict value is %s") % predict_value

    logging.debug('The API has been called with %s' % request.form)
    return render_template('api_page.html', form=form,query_string=query)
    

#@app.route('/products/widget1')
#def products_widget1():
#    return  "Hello Products widget1"




class InputLabelForm(FlaskForm):
    query_string = StringField(" ",validators=[DataRequired()])
    submit = SubmitField('submit')
    


if __name__=='__main__':
    app.run(host='127.0.0.1', port='5005',debug=True)



