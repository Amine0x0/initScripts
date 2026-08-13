#!/bin/bash

set -e

INSTALL_PATH="/goinfre/amabbadi/"
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

curl -L -o vscode-linux-x64.tar.gz "https://update.code.visualstudio.com/latest/linux-x64/stable"
tar -xzf vscode-linux-x64.tar.gz

rm -rf "$INSTALL_PATH/VSCode-linux-x64"

mv ./VSCode-linux-x64 "$INSTALL_PATH/"
rm -rf "$TMP_DIR"
