from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

class Review(BaseModel):
    id: Optional[int] = None
    lot: str
    time: str
    rating: int


with open('reviews.json', 'r') as f:
    reviews =  json.load(f)
    print("reviews:")
    print(reviews)
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
        print(review['lot'] + '\n' + lot_name)
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
    print(review_to_add)
    reviews.append(review_to_add)
    print(reviews)

    with open('reviews.json', 'w') as f:
        json.dump(reviews, f)
