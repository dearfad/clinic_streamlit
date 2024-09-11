from libs.bvcutils import read_models

data = read_models()

data.to_excel('data/models.xlsx', index=False)

