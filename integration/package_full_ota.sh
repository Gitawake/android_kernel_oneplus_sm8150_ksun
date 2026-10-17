#!/usr/bin/env bash
# Run after integrating and AVB-packing the offline filesystem copies.
# Arguments: workspace root, avbroot executable. Signing keys stay local.
set -euo pipefail
task_root=$(cd "$1" && pwd)
task_avbroot=$2
cd "$task_root"
"$task_avbroot" ota patch \
  --input los24-20261016/lineage-24.0-20261016-nightly-hotdog-verified.zip \
  --output release-candidate-los24-20261016/lineage-24.0-20261016-hotdog-ksun-v3.4.2-gapps-gboard.zip \
  --key-avb los24-20261016/signing-private/avb.key \
  --key-ota los24-20261016/signing-private/ota.key \
  --cert-ota los24-20261016/ota.crt \
  --rootless \
  --replace boot los24-20261016/modified/boot.img \
  --replace system los24-20261016/modified/system.img \
  --replace product los24-20261016/modified/product.img \
  --replace system_ext los24-20261016/modified/system_ext.img \
  --clear-vbmeta-flags --zip-mode seekable
# --rootless only skips automatic Magisk injection. The replacement boot
# already contains the compiled-in KernelSU Next release port.
"$task_avbroot" ota verify \
  --input release-candidate-los24-20261016/lineage-24.0-20261016-hotdog-ksun-v3.4.2-gapps-gboard.zip \
  --cert-ota los24-20261016/ota.crt \
  --public-key-avb los24-20261016/avb-public.bin
