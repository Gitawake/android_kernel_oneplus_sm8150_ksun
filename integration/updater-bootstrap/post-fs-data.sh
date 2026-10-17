#!/system/bin/sh
MODDIR=${0%/*}
[ "$(getprop ro.lineage.device)" = hotdog ] || exit 0
[ "$(getprop ro.build.version.sdk)" = 36 ] || exit 0
STORE="$MODDIR/otacerts.zip"
TARGET=/system/etc/security/otacerts.zip
chcon u:object_r:system_file:s0 "$STORE" || exit 1
# Explicit bind mount avoids a dependency on a particular KSU metamodule.
BB=/data/adb/ksu/bin/busybox
if [ -x "$BB" ]; then
  "$BB" nsenter -t 1 -m -- "$BB" mount -o bind "$STORE" "$TARGET"
else
  mount -o bind "$STORE" "$TARGET"
fi
