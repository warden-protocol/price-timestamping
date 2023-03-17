#!/bin/bash
set -euxo pipefail
docker ps --all --quiet | xargs docker rm --force
docker system prune --volumes --all --force
