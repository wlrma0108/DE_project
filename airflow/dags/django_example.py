from __future__ import annotations
import os, sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# ── Django import 준비 ─────────────────────────────────
DJANGO_PROJECT_PATH = "/opt/django"
if DJANGO_PROJECT_PATH not in sys.path:
    sys.path.append(DJANGO_PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.core.management import call_command
from places.models import Spot

# ── Task funcs ────────────────────────────────────────
def load_spots_via_management():
    # Django 관리명령 실행
    call_command("load_spots")

def print_spot_count():
    print("Spot count:", Spot.objects.count())
    for s in Spot.objects.order_by("-rating")[:5]:
        print(" -", s.name, s.rating)

# ── DAG 정의 ─────────────────────────────────────────
default_args = {
    "owner": "airflow",
    "retries": 0,
}

with DAG(
    dag_id="django_etl_demo",
    default_args=default_args,
    schedule=timedelta(hours=12),  # 12시간마다
    start_date=datetime(2025, 7, 29),  # 여러분 환경에 맞춰 조정 가능
    catchup=False,
    tags=["django", "etl"],
) as dag:

    t1 = PythonOperator(
        task_id="load_spots",
        python_callable=load_spots_via_management,
    )

    t2 = PythonOperator(
        task_id="print_count",
        python_callable=print_spot_count,
    )

    t1 >> t2
