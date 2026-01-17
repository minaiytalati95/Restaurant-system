from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.menu import api as menu_router
from app.api.orders import api as orders_router
from app.api.customers import api as customers_router

app = FastAPI(title="Restaurant Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(menu_router, tags=["Menu"])
app.include_router(orders_router, tags=["Orders"])
app.include_router(customers_router, tags=["Customers"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
