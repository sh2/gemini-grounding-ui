#!/bin/bash

exec streamlit run gemini-grounding-ui.py \
    --browser.gatherUsageStats=false \
    --server.baseUrlPath=/grounding-gemini \
    --server.address 10.0.2.100 \
    --server.port 8501
