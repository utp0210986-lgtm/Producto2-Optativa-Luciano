from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.restaurants import router as restaurants_router
from app.services.restaurant_service import RestaurantService

app = FastAPI(title="FriendlyEats FastAPI")
app.include_router(restaurants_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")
service = RestaurantService()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def home(
    request: Request,
    city: str = "",
    category: str = "",
    price: str = "",
    order_by: str = "name",
):
    if order_by not in ("name", "avgRating"):
        order_by = "name"
    restaurants = service.list(
        city=city.strip() or None,
        category=category.strip() or None,
        price=int(price) if price in ("1", "2", "3") else None,
        order_by=order_by,
    )
    filters = {"city": city, "category": category, "price": price, "order_by": order_by}
    return templates.TemplateResponse(
        request, "restaurants.html", {"restaurants": restaurants, "filters": filters}
    )


@app.get("/restaurants/new")
async def new_restaurant(request: Request):
    return templates.TemplateResponse(request, "restaurant_form.html", {"restaurant": None})


@app.get("/restaurants/{restaurant_id}")
async def restaurant_detail(request: Request, restaurant_id: str):
    restaurant = service.get(restaurant_id)
    return templates.TemplateResponse(request, "restaurant_detail.html", {"restaurant": restaurant})


@app.get("/restaurants/{restaurant_id}/edit")
async def edit_restaurant(request: Request, restaurant_id: str):
    restaurant = service.get(restaurant_id)
    return templates.TemplateResponse(request, "restaurant_form.html", {"restaurant": restaurant})
