from fastapi import FastAPI

from online_store.router import router as router_store

app = FastAPI(
    title="Online Store"
)

app.include_router(router_store)
