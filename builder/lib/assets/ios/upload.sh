#!/usr/bin/env bash
echo fastlane deliver \
-u "$APPLE_ID" \
-a "$BUNDLE" \
-i "$IPA_PATH" \
-e "$TEAM_NAME" \
-z "$APP_VERSION" \
--skip_screenshots \
--skip_metadata

fastlane deliver \
-u "$APPLE_ID" \
-a "$BUNDLE" \
-i "$IPA_PATH" \
-e "$TEAM_NAME" \
-z "$APP_VERSION" \
--skip_screenshots \
--skip_metadata
