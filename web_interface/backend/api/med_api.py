# Create a REST API which takes form POST and returns JSON
# Use FAST API for creating endpoint

import json
import os
import sys
import base64
from urllib import response
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
from api_adapter import api_adapter_cb
app=FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    # wildcard for testing on local network
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"med_api_version": "1.0.0 Alpha"}
@app.get("/api_status")
async def api_status():
    return {"status": "OK"}
class Data(BaseModel):
    models: str
    models2: str
    checkbox: str
# Aceept form POST and return JSON
@app.post("/med_data")
async def med_data(data: Data):
    req_data=data.dict()
    print(req_data)
    checkbox=req_data["checkbox"]
    models1=req_data["models"]
    models2=req_data["models2"]
    models=[]
    models.append(models1)
    models.append(models2)
    if checkbox == "False":
        med_data = med_nocompare(models1)
        return med_data
    best_acc=0
    best_model=None
    model1=40
    model2=60
    random_pred="Alcohol Disorder"
    random_pred2="Pyschiatric disorder"
    api_adapter_cb_obj=api_adapter_cb()
    model_results=api_adapter_cb_obj.model_selection(models)
    if model_results is not None:
        # add {"response_msg": response_msg} to the model_results dict
        response_msg="OK"
        model_results["response_msg"]=response_msg
        with open(model_results["compare_img"]["model1"], "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())
        with open(model_results["compare_img"]["model2"], "rb") as image_file:
            encoded_image2 = base64.b64encode(image_file.read())
        model_results["compare_img"]["model1"]=encoded_image
        model_results["compare_img"]["model2"]=encoded_image2
        return model_results
    else:
        response_msg="Model not found"
        final_result={"response_msg": response_msg}
        return final_result



  
    # update best_model and best_acc by comparing model1 and model2

    return model_results
def med_nocompare(model_name):
    acc=0
    image=None
    random_pred="Insomnia Disorder"
    response_msg="None"
    encoded_image="None"
    model_list=[]
    model_list.append(model_name)
    print("data",model_list)
    api_adapter_cb_obj=api_adapter_cb()
    model_results=api_adapter_cb_obj.model_selection(model_list)
    print(model_results["accuracy"])
    if model_results is not None:
        # rf_result=dict(zip(['accuracy_rf','prediction_rf','image_rf'],rf_result))
        acc=model_results["accuracy"]
         # open image and convert to base64
        with open(model_results["image"], "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())
        image=encoded_image
        random_pred=model_results["prediction"]
        response_msg="OK"
        # create dictionary with above values
        final_result={"best_acc": acc, "img": image, "pred": random_pred, "response_msg": response_msg}
    else:
        response_msg="Model not found"
        final_result={"response_msg": response_msg} 
    
    return final_result