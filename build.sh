#!/bin/bash

YYYYMMDD=$(date +%Y%m%d)

podman build --tag gemini-grounding-ui:${YYYYMMDD} .
