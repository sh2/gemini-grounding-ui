#!/bin/bash

export GEMINI_API_KEY=

streamlit run src/gemini-grounding-ui.py \
    --browser.gatherUsageStats=false \
