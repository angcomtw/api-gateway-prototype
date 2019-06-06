# -*- coding: utf-8 -*-
import pandas as pd
import psycopg2

# psycopg2的應用
# 取得連結
def get_conn():
    conn = psycopg2.connect(database="postgres",host="192.168.43.236",port="5432",user="postgres",password="crv1313")
    # host="10.211.55.11"
    return conn

def get_model_data(conn):
    sql = "SELECT id, age, education, annualincome, loanlimit, rate from loan_price"
    df = pd.read_sql(sql, conn)
    return df

def get_data_by_id(conn, id):
    sql = "SELECT id, age, education, annualincome from loan_price WHERE id = %(id)s"
    df = pd.read_sql(sql, conn, params={"id":id})
    return df


