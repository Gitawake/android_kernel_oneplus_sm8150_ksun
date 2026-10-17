#!/system/bin/sh
MODDIR=${0%/*}
while [ "$(getprop sys.boot_completed)" != 1 ]; do sleep 2; done
[ "$(getprop ro.lineage.device)" = hotdog ] || exit 0
SDK=$(getprop ro.build.version.sdk)
if [ "$SDK" = 36 ]; then
  setprop lineage.updater.allow_major_upgrades true
  exit 0
fi
[ "$SDK" = 37 ] || exit 0
setprop lineage.updater.allow_major_upgrades false
IME=com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME
if ime list -s | grep -Fxq "$IME"; then
  ime enable "$IME" && ime set "$IME" && touch "$MODDIR/ime-configured"
fi
# The new ROM carries the OTA certificate itself. Preparation is one-time only.
[ -f "$MODDIR/ime-configured" ] && touch "$MODDIR/disable"
