#!/bin/bash

alembic upgrade 4b46a664ca10
alembic upgrade head

gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000