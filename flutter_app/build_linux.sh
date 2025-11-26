#!/bin/bash
set -e

cd "$(dirname "$0")"
flutter build linux --release
