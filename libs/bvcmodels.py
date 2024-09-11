import importlib

def chat(patient):
    model = importlib.import_module(f"libs.platforms.{patient.model.module}")
    return model.chat(patient)
