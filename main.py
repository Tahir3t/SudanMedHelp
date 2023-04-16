import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype)
import numpy as np
import time
from google.oauth2 import service_account
from gspread_pandas import Spread, Client
import streamlit as st
# import gspread
# from gspread_dataframe import get_as_dataframe

st.set_page_config(layout='wide', page_title="Khartoum Medical Response", initial_sidebar_state="expanded")
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 20px;
}
#MainMenu {visibility: hidden;}
footer {visibility: visible;}
footer:after{content:'Twitter: @Tahir3T'; display:block; position:relative}
</style>
""",
    unsafe_allow_html=True,
)

st.title("دليل الكوادر للمساعدة الطبية والنفسية - ولاية الخرطوم ⚕️")
st.write('''
        في ظل الظروف العصيبة التي تمر بها البلاد، تزداد الحوجة للعناية الطبية والنفسية. بين يديكم دليل للمتطوعين من الكوادر الطبية بولاية الخرطوم ...
         واذا كنتم تريدون التطوع، الرجاء ملئ الاستمارة ادناه لاضافة بياناتكم لهذا الموقع
            ''')
st.write("https://forms.gle/Nm8qT8D3mVq6tX6b7")

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = scope)

client = Client(scope=scope, creds=credentials)
spreadsheetname = "Sudan Medical Help (Responses)"
spread = Spread(spreadsheetname, client=client)
data = spread.sheet_to_df(sheet="Form Responses 1", index=0)
# gc = gspread.service_account("credentials.json")
# ws_info = gc.open("Sudan Medical Help (Responses)").worksheet("Form Responses 1")
# data = get_as_dataframe(ws_info)
data = data.loc[:, ~data.columns.str.contains("^Unnamed")]
data = data[data['Timestamp'].notna()]
data = data.fillna("-")
data['رقم الهاتف'] = data['رقم الهاتف'].astype(str).apply(lambda x: x.replace('.0',''))
data['رقم الهاتف'] = data['رقم الهاتف'].str.zfill(10)
data['مواعيد الاتصال من الساعة'] = data['مواعيد الاتصال من الساعة'].astype(str).apply(lambda x: x.replace('0:0',''))
df = data.copy()


seach_filter = ["المجال", "المدينة", "نوع المساعدة"]

modification_container = st.container()
with modification_container:
    st.sidebar.header("⚕️ الخيارات")
    st.markdown("##")
    to_filter_columns = st.sidebar.multiselect("ابحث بواسطة:", seach_filter)
    for column in to_filter_columns:
        left, right = st.sidebar.columns((1,20))
        left.write("↳")
        if is_categorical_dtype(df[column]) or df[column].nunique()<=12:
            user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].unique(),
                default=list(df[column].unique())
            )
            df = df[df[column].isin(user_cat_input)]

        elif is_numeric_dtype(df[column]):
            _min = int(df[column].min())
            _max = int(df[column].max())
            user_num_input = right.slider(
                f"Values for {column}",
                _min,
                _max,
                (_min, _max)
            )
            df = df[df[column].between(*user_num_input)]
        else:
            user_text_input = right.text_input(
                f"Substring or regex in {column}"
            )
            if user_text_input:
                df = df[df[column].str.contains(user_text_input)]

print(data)

kht_meds = df[df['المدينة'] == "الخرطوم"]["الاسم"].nunique()
bahri_meds = df[df['المدينة'] == "بحري"]["الاسم"].nunique()
omdurman_meds = df[df['المدينة'] == "امدرمان"]["الاسم"].nunique()



st.markdown("#### عدد الكوادر الطبية المتطوعة")
b1, b2, b3 = st.columns(3)
with b1:
    st.metric("الخرطوم", kht_meds)
with b2:
    st.metric("بحري", bahri_meds)
with b3:
    st.metric("امدرمان", omdurman_meds)
st.markdown("---")

st.markdown("#### بيانات الكوادر الطبية")
for index, row in df.iterrows():
    with st.expander(row['الاسم']):
        x1, x2 = st.columns(2)
        with x1:
            st.metric("الاسم", row['الاسم'])
            st.metric("المجال", row['المجال'])
            st.metric("التخصص", row['التخصص'])
            st.metric("المدينة", row['المدينة'])
            st.metric("المنطقة داخل المدينة", row['المنطقة داخل المدينة'])      
        with x2:
            st.metric("رقم الهاتف", row['رقم الهاتف'])
            st.metric("نوع الاتصال", row['نوع الاتصال'])
            st.metric("مواعيد الاتصال من الساعة", row['مواعيد الاتصال من الساعة'])
            st.metric("نوع المساعدة", row['نوع المساعدة'])
            st.metric("معلومات اخرى ", row['معلومات اخرى '])

st.markdown("---")
