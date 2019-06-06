# coding:utf-8

from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
import pandas as pd
import pgsqlhelper

#讀取training資料
conn = pgsqlhelper.get_conn()
training_data = pgsqlhelper.get_model_data(conn)
conn.close()

#traintrain看
X = training_data[['age', 'education', 'annualincome']]
y = training_data[['loanlimit']]
linreg = LinearRegression()
linreg.fit(X, y)

#保存模型
joblib.dump(linreg, '/api/MLaaS_gatewayv1/filename.pkl')

#用模型檔進行預測
#[[21627091.91695168]]
clf = joblib.load('/api/MLaaS_gatewayv1/filename.pkl')
predit_X = [[30,1,50]]
print(clf.predict(predit_X))

