import crud
import schemas
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from models import metadata
from database import engine, SessionMaker
from sqlalchemy.orm import Session
from typing import Union

app = FastAPI()
metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()


@app.get('/queryRank/{date}', response_model=list[schemas.RankDetail])
def getRanDetail(date: str, page: Union[int, None] = None, db: Session = Depends(get_db)):
    if not page:
        page = 0
    rank_details = crud.get_rank_details(db, date, page=page)
    if rank_details is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return rank_details


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
