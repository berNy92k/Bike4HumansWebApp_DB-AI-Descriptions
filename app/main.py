from fastapi import FastAPI

from app.routers.init_routers import init_routers, init_pre_requested_methods, init_pages

app = FastAPI()

init_pre_requested_methods(app)
init_pages(app)
init_routers(app)









# In case you want to use auto create of db uncomment code below
# from app.database.database import Base, engine
# from app.models.role import Role
# from app.models.user import User

# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)
