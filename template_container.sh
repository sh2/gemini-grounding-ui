#!/bin/bash

podman run \
        --detach \
        --restart=always \
        --publish=8501:8501 \
        --env=GEMINI_API_KEY= \
        --name=gemini-grounding-ui \
        gemini-grounding-ui:20250101
