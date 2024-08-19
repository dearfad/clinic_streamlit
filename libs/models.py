import importlib

SERVER_MODEL_DICT = {
    'tongyi': 'XingChen',
    'baichuan': "BaiChuan",
}

def load_model(server, model):
    Model = importlib.import_module(model, package=f"libs.servers.{server}")
    return Model()

model = load_model(server="tongyi", model="XingChen")
