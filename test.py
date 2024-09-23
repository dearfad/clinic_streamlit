from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 创建数据库引擎
engine = create_engine('sqlite:///data/clinic.db')

# 创建基类
class Base(DeclarativeBase):
    pass

# 创建元数据对象
metadata = MetaData()

# 使用反射加载表结构
metadata.reflect(engine, only=['model'])

# 将反射得到的表结构转化为 ORM 类
class Model(Base):
    __table__ = metadata.tables['model']
    __table__.primary_key.columns = "id"

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 现在你可以使用 YourModelName 类来操作数据库了
# 例如，查询所有记录
results = session.query(Model).all()
for instance in results:
    print(instance)  # 'instance' 是 YourModelName 类型的对象

# 关闭会话
session.close()