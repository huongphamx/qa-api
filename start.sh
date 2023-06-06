#! /usr/bin/env sh
set -e

. /app/prestart.sh

exec uvicorn app.main:app --host 0.0.0.0 --reload
