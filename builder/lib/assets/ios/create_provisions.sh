#!/usr/bin/env bash
echo fastlane sigh \
--app_identifier "$BUNDLE" \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--provisioning_name "$PROVISION_NAME_PROD" \
--filename "$OUTPUT_NAME_PROD" \
--output_path "$OUTPUT_PATH" \
--adhoc \
--force

fastlane sigh \
--app_identifier "$BUNDLE" \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--provisioning_name "$PROVISION_NAME_PROD" \
--filename "$OUTPUT_NAME_PROD" \
--output_path "$OUTPUT_PATH" \
--adhoc \
--force

echo fastlane sigh \
--app_identifier "$BUNDLE" \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--provisioning_name "$PROVISION_NAME_DEV" \
--filename "$OUTPUT_NAME_DEV" \
--output_path "$OUTPUT_PATH" \
--development \
--force

fastlane sigh \
--app_identifier "$BUNDLE" \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--provisioning_name "$PROVISION_NAME_DEV" \
--filename "$OUTPUT_NAME_DEV" \
--output_path "$OUTPUT_PATH" \
--development \
--force

echo fastlane sigh \
--app_identifier "$BUNDLE" \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--provisioning_name "$PROVISION_NAME_APPSTORE" \
--filename "$OUTPUT_NAME_APPSTORE" \
--output_path "$OUTPUT_PATH" \
--force

fastlane sigh \
--app_identifier "$BUNDLE" \
--username "$APPLE_ID" \
--team_name "$TEAM_NAME" \
--platform "$PLATFORM" \
--provisioning_name "$PROVISION_NAME_APPSTORE" \
--filename "$OUTPUT_NAME_APPSTORE" \
--output_path "$OUTPUT_PATH" \
--force
