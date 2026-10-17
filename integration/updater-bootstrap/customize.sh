#!/system/bin/sh
[ "$BOOTMODE" = true ] || abort "Install this preparation module in KernelSU while Android is running."
case "$(getprop ro.lineage.device)" in hotdog) ;; *) abort "Only OnePlus 7T Pro / hotdog is supported." ;; esac
[ "$(getprop ro.build.version.sdk)" = 36 ] || abort "This preparation module is only for LOS 23 / Android 16."
case "$(getprop ro.lineage.version)" in 23.2-20260925-*) ;; *) abort "This package is scoped to the verified LOS 23.2-20260925 starting build." ;; esac
[ -f /system/etc/security/otacerts.zip ] || abort "Missing system OTA trust store."
cp /system/etc/security/otacerts.zip "$MODPATH/original-otacerts.zip"
set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/post-fs-data.sh" 0 0 0755
set_perm "$MODPATH/service.sh" 0 0 0755
ui_print "After reboot: Settings > System > Updater > Local update."
ui_print "The complete ROM ZIP is installed by the original LOS updater."
