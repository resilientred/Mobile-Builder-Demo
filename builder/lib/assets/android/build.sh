#!/usr/bin/env bash
cd $FINAL_PATH
./gradlew assembleRelease -Pandroid.injected.signing.store.file=$KEY_FILE \
-Pandroid.injected.signing.store.password=$FILE_PASS \
-Pandroid.injected.signing.key.alias=$KEY_ALIAS \
-Pandroid.injected.signing.key.password=$ALIAS_PASS