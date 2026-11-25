
#!/bin/bash
set -euo pipefail

BUCKET="devops-cicd-production-251126"
REGION="ap-southeast-2"
APP_DIR="/opt/devops-app"
ARTIFACT="${1:?Build artifact required}"
TEMP_DIR=$(mktemp -d)

trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Downloading build from AWS S3..."
aws s3 cp "s3://$BUCKET/$ARTIFACT" \
    "$TEMP_DIR/build.zip" --region "$REGION"

echo "Extracting application..."
unzip -o "$TEMP_DIR/build.zip" -d "$TEMP_DIR/release"

echo "Installing application..."
mkdir -p "$APP_DIR"
cp -r "$TEMP_DIR/release/." "$APP_DIR/"
chown -R ubuntu:ubuntu "$APP_DIR"

echo "Installing Python dependencies..."
runuser -u ubuntu -- python3 -m venv "$APP_DIR/venv"
runuser -u ubuntu -- "$APP_DIR/venv/bin/pip" install \
    -r "$APP_DIR/requirements.txt"

echo "Restarting production application..."
systemctl restart devops-app
systemctl is-active devops-app

echo "Checking application health..."
curl --fail --retry 10 --retry-delay 2 \
    --retry-connrefused http://127.0.0.1/health

echo "Deployment completed successfully!"
