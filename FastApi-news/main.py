import uvicorn
from fastapi import FastAPI

from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许的源
    allow_credentials=True,     # 允许携带cookie
    allow_methods=["*"],        # 允许的请求方法
    allow_headers=["*"],        # 允许的请求头
)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run(app)