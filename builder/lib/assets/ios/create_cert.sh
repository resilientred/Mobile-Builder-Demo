#!/usr/bin/env bash

fastlane pem \
-a "$BUNDLE" \
-u "$APPLE_ID" \
-p "$CERT_PASS" \
-o "$CERT_FILE_NAME" \
-l "$TEAM_NAME" \
-e "$OUTPUT_PATH" \
--force
