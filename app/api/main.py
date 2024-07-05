import csv
from io import StringIO
from collections import defaultdict
from fastapi import Depends, FastAPI, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.api import crud, models, schemas, dependencies
from app.core.db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/attacks/", response_model=list[schemas.Attack])
def read_attacks(
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)
):
    attacks = crud.get_attacks(db, skip=skip, limit=limit)
    return attacks


@app.post("/attacks/", response_model=list[schemas.Attack])
def read_attacks_from_file(
    file: UploadFile, db: Session = Depends(dependencies.get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Not CSV file")

    data = defaultdict(list)
    file_bytes = file.file.read()
    buffer = StringIO(file_bytes.decode("utf-8"))
    csv_reader = csv.DictReader(buffer)
    for row in csv_reader:
        key = row["saddr"]
        data[key].append(float(row["dur"]))
    buffer.close()
    file.file.close()

    added_data = crud.update_attacks(db, data)
    return added_data
