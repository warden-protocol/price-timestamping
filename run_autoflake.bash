#!/bin/bash
set -euxo pipefail
autoflake \
  --recursive \
  --remove-all-unused-import \
  --expand-star-imports \
  --ignore-init-module-imports \
  --remove-duplicate-keys \
  --remove-unused-variables \
  --remove-rhs-for-unused-variable \
  --in-place \
  .
