from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class FoodItem(BaseModel):
    id: int
    name: str
    description: str
    price: float

# Sample database
food_items = [
    {"id": 1, "name": "Pizza", "description": "Delicious cheese pizza", "price": 12.99},
    {"id": 2, "name": "Burger", "description": "Juicy beef burger", "price": 8.99}
]

@app.get("/foods/", response_model=List[FoodItem])
async def get_food_items():
    return food_items

@app.post("/foods/", response_model=FoodItem)
async def create_food_item(food_item: FoodItem):
    food_items.append(food_item.dict())
    return food_item

@app.put("/foods/{food_id}", response_model=FoodItem)
async def update_food_item(food_id: int, food_item: FoodItem):
    for index, item in enumerate(food_items):
        if item["id"] == food_id:
            food_items[index] = food_item.dict()
            return food_item
    return {"error": "Food item not found"}

@app.patch("/foods/{food_id}", response_model=FoodItem)
async def partial_update_food_item(food_id: int, food_item: FoodItem):
    for index, item in enumerate(food_items):
        if item["id"] == food_id:
            food_items[index].update(food_item.dict(exclude_unset=True))
            return food_items[index]
    return {"error": "Food item not found"}

@app.delete("/foods/{food_id}", response_model=dict)
async def delete_food_item(food_id: int):
    for index, item in enumerate(food_items):
        if item["id"] == food_id:
            food_items.pop(index)
            return {"message": f"Food item {food_id} deleted"}
    return {"error": "Food item not found"}