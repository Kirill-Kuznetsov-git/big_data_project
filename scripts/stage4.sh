#!/bin/bash

sudo fuser -k 60000/tcp
streamlit run scripts/dashboard.py --server.port 60000
