#!/bin/bash
set -euxo pipefail
docker compose --file priceapi/fastapi/app/docker-compose.yml build
docker compose --file priceapi/fastapi/app/docker-compose.yml up
