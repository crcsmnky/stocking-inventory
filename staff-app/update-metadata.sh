#!/bin/bash

set -e

TOKEN=${1}

echo "=== Updating Project Metadata ==="

echo "staff-app-token=${TOKEN}"
gcloud compute project-info add-metadata --metadata staff-app-token=${TOKEN}

echo "=== Project Metadata Updated ==="
