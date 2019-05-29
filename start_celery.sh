#!/usr/bin/env bash

# Commands to run celery workers and beat

# celery -A cert_app worker -l debug --concurrency=1

celery -A cert_app worker -l debug -n worker.high -Q high &
celery -A cert_app worker -l debug -n worker.normal -Q normal &
celery -A cert_app worker -l debug -n worker.low -Q low &
celery beat -A cert_app -l debug &