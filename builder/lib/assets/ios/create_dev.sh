#!/usr/bin/env bash

echo fastlane cert \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--output_path "$OUTPUT_PATH"

fastlane cert \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--output_path "$OUTPUT_PATH"

echo fastlane cert \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--output_path "$OUTPUT_PATH"
--development

fastlane cert \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--output_path "$OUTPUT_PATH"
--development
