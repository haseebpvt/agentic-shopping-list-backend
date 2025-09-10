import uvicorn
from fastapi import FastAPI

from server.route.preferences_route import router as preference_route
from server.route.product_recommendation_route import router as product_recommendation_route
from server.route.shopping_list_route import router as shopping_list_route
from server.route.extractor_route import router as extractor_route

app = FastAPI()

app.include_router(product_recommendation_route, prefix="/recommend", tags=["Recommend"])
app.include_router(preference_route, prefix="/preference", tags=["Preference"])
app.include_router(shopping_list_route, prefix="/shopping_list", tags=["ShoppingList"])
app.include_router(extractor_route, prefix="/extractor", tags=["Extractor"])


@app.get("/")
def read_root():
    return {"Hello": "World x"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")
