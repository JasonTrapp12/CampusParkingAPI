from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: Optional[int] = None
    lot: str
    time: str
    rating: int


with open('reviews.json', 'r') as f:
    reviews =  json.load(f)
    f.close()


def get_review(r_id: int):
    for review in reviews:
        if review['id'] == r_id:
            return review     
    return {}

@app.get('/reviews/{lot_name}')
def get_lot_reviews(lot_name: str):
    lot_reviews = []
    for review in reviews:
        if review['lot'] == lot_name:
            lot_reviews.append(review)
    return lot_reviews

@app.post('/addReview', status_code=201)
def post_review(new_review: Review):
    max = -1
    for review in reviews:
        if review['id'] > max:
            max = review['id']
    id = max + 1
    print(id)
    review_to_add = {
        "id" : id,
        "lot" : new_review.lot,
        "time" : new_review.time,
        "rating" : new_review.rating
    }
    reviews.append(review_to_add)

    with open('reviews.json', 'w') as f:
        json.dump(reviews, f)
