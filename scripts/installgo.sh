#!/bin/bash

set -e

INSTALL_PATH="/goinfre/amabbadi/tools"
TMP_DIR=$(mktemp -d)

cd "$TMP_DIR"

wget -O go.tar.gz "https://go.dev/dl/go1.26.5.linux-amd64.tar.gz"

mkdir -p "$INSTALL_PATH"
rm -rf "$INSTALL_PATH/go"

tar -xzf ./go.tar.gz
mv ./go "$INSTALL_PATH/"

rm -rf "$TMP_DIR"

PROFILE_FILE="$HOME/.zshrc"

GO_BIN="$INSTALL_PATH/go/bin"
GO_USER_BIN="$HOME/go/bin"

if ! grep -q "$GO_BIN" "$PROFILE_FILE"; then
    echo "" >> "$PROFILE_FILE"
    echo "# Added by Go installer script" >> "$PROFILE_FILE"
    echo "[[ \":\$PATH:\" != *\":$GO_USER_BIN:\"* ]] && export PATH=\"$GO_USER_BIN:\$PATH\"" >> "$PROFILE_FILE"
    echo "[[ \":\$PATH:\" != *\":$GO_BIN:\"* ]] && export PATH=\"$GO_BIN:\$PATH\"" >> "$PROFILE_FILE"
    echo "Path appended and guarded against duplication in $PROFILE_FILE"
fi

export PATH="$GO_USER_BIN:$GO_BIN:$PATH"