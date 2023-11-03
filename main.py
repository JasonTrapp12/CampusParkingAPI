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
    reviews = json.load(f)
    f.close()


def get_review(r_id: int):
    for review in reviews:
        if review['id'] == r_id:
            return review
    return {}


@app.get('/reviews/{lot_name}')
def get_lot_reviews(lot_name: str):
    lot_reviews = {
        "8-9AM": 0,
        "9-10AM": 0,
        "10-11AM": 0,
        "11-12PM": 0,
        "12-1PM": 0,
        "1-2PM": 0,
        "2-3PM": 0,
        "3-4PM": 0
    }

    lot_reviews_keys = lot_reviews.keys()
    for time in lot_reviews_keys:
        num_reviews = 0
        for review in reviews:
            if review['lot'] == lot_name and review['time'] == time:
                lot_reviews[time] += review['rating']
                num_reviews += 1
        if num_reviews > 0:
            lot_reviews[time] = lot_reviews[time] / num_reviews
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
        "id": id,
        "lot": new_review.lot,
        "time": new_review.time,
        "rating": new_review.rating
    }
    reviews.append(review_to_add)

    with open('reviews.json', 'w') as f:
        json.dump(reviews, f)
