#!/usr/bin/env bash

echo fastlane gym \
--workspace "$WORKSPACE_PATH" \
--scheme "$BUILD_SCHEME" \
--output_directory "$OUTPUT_PATH" \
--output_name "$OUTPUT_NAME" \
--export_method app-store \
--clean

fastlane gym \
--workspace "$WORKSPACE_PATH" \
--scheme "$BUILD_SCHEME" \
--output_directory "$OUTPUT_PATH" \
--output_name "$OUTPUT_NAME" \
--export_method app-store \
--clean
