from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import router
from src.db.database import Base, engine




version = "v1"

app = FastAPI(
    title="Bookly CRUD",
    description="A REST API for a book review web service",
    version=version,
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



app.include_router(book_router,prefix=f"/api/{version}/books",tags=["books"])
app.include_router(router,prefix=f"/api/{version}/auth",tags=["Authentication"])


