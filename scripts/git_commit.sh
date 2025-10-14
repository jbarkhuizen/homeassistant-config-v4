#!/bin/bash
cd /config
git add .
git commit -m "Auto commit from Home Assistant: $(date '+%Y-%m-%d %H:%M:%S')"
git push