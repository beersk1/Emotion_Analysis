# Core Pkgs
import streamlit as st 
import altair as alt
from lime.lime_text import LimeTextExplainer
from lime.lime_text import IndexedString,IndexedCharacters
from lime.lime_base import LimeBase
from matplotlib import pyplot as plt
import boto3
import tempfile
# EDA Pkgs
import pandas as pd 
import numpy as np 
from datetime import datetime


# Utils
import joblib 

def make_prediction():
    # connect to s3 bucket with the access and secret access key
    client = boto3.client(
        's3', aws_access_key_id=st.secrets["access_key"],aws_secret_access_key=st.secrets["secret_access_key"],region_name='ap-south-1')

    bucket_name = "nlpmodelsnp"
    key = "model1.pickle"

    # load the model from s3 in a temporary file
    with tempfile.TemporaryFile() as fp:
        # download our model from AWS
        client.download_fileobj(Fileobj=fp, Bucket=bucket_name, Key=key)
        # change the position of the File Handle to the beginning of the file
        fp.seek(0)
        # load the model using joblib library
        model = joblib.load(fp)

    # prediction from the model, returns 0 or 1
    return model

model = make_prediction()
st.set_page_config(layout="wide")

# Track Utils
# from track_utils import create_page_visited_table,add_page_visited_details,view_all_page_visited_details,add_prediction_details,view_all_prediction_details,create_emotionclf_table

# Fxn
def predict_emotions(docx):
	results = model.predict([docx])
	return results[0]

def get_prediction_proba(docx):
	results = model.predict_proba([docx])
	return results

emotions_emoji_dict = {"anger":"😠", "fear":"😨😱", "joy":"😂", "love":"❤️", "sadness":"😔","surprise":"😮"}

# Main Application

st.title("Emotion Classifier App")

st.subheader("Home-Emotion In Text")
with st.form(key='emotion_clf_form'):
	raw_text = st.text_area("Type Here")
	submit_text = st.form_submit_button(label='Submit')
if submit_text:
	col1,col2  = st.columns(2)
	# Apply Fxn Here
	prediction = predict_emotions(raw_text)
	probability = get_prediction_proba(raw_text)
	
	# add_prediction_details(raw_text,prediction,np.max(probability),datetime.now())
	with col1:
		st.success("Original Text")
		st.write(raw_text)
		st.success("Prediction")
		emoji_icon = emotions_emoji_dict[prediction]
		st.write("{}:{}".format(prediction,emoji_icon))
		st.write("Confidence:{}".format(np.max(probability)))
	with col2:
		st.success("Prediction Probability")
		# st.write(probability)
		proba_df = pd.DataFrame(probability,columns=model.classes_)
		# st.write(proba_df.T)
		proba_df_clean = proba_df.T.reset_index()
		proba_df_clean.columns = ["emotions","probability"]
		fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions',y='probability',color='emotions')
		st.altair_chart(fig,use_container_width=True)
	explainer_LR = LimeTextExplainer(class_names=model.classes_)
	idx  = 15
		# print("Actual Text : ", X_test[idx])
		# print("Prediction : ", RF.predict(X_test)[idx])
		# print("Actual :     ", y_test[idx])
	exp = explainer_LR.explain_instance(raw_text, model.predict_proba,top_labels=5)
	html = exp.as_html()
	import streamlit.components.v1 as components
	components.html(html, height=1500)
