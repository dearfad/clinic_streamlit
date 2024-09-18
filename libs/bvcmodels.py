import importlib

def chat(module, modelname, messages):
    model = importlib.import_module(f"libs.platforms.{module}")
    return model.chat(modelname, messages)

def chat_patient(patient):
    return chat(patient.model.module, patient.model.name, patient.messages)


