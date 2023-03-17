#!/bin/bash
set -euxo pipefail
docker compose --file etl_pricedumping/docker-compose.yml build
docker compose --file etl_pricedumping/docker-compose.yml up
