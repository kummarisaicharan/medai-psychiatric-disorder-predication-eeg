import os
import sys
# pop the appendix of the file name
sys.path.insert(0,'../')
from models.rf_model import RF_Model_cb
from models.r_som_model import SOM_Model_cb
from models.svc_model import SVC_Model_cb

class api_adapter_cb:
    def model_selection(self,models):
        print(models)

        if len(models) == 2:
            return api_adapter_cb.models_compare(models)
        else:
            model_name=models[0]
        # write a switch case for the model name
        if model_name == "rf_model":
            return RF_Model_cb.rf_model()
        elif model_name=="som_model":
            return SOM_Model_cb.som_model()
        elif model_name=="svc_model":
            return SVC_Model_cb.svc_model()
        else:
            return None
    def models_compare(models):
        model1=models[0]
        model2=models[1]
        # convert model1 to list
        model1_list=model1.split(",")  
        # convert model2 to list
        model2_list=model2.split(",")

        model1=api_adapter_cb().model_selection(model1_list)
        
        model2=api_adapter_cb().model_selection(model2_list)
        if(model1==None or model2==None):
            return None
        else:
            return {"model1": model1["accuracy"], "model2": model2["accuracy"],"compare":{"model1":model1["prediction"],"model2":model2["prediction"]},"compare_img":{"model1":model1["image"],"model2":model2["image"]}}
        
# models=["rf_model","som_model"]
# api_obj=api_adapter_cb()
# print(api_obj.model_selection(models))
        

            