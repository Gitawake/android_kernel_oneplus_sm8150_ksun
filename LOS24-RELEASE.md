# LOS 24.0-20261016 / hotdog / KernelSU Next v3.4.2

This branch builds the official v3.4.2 release kernel port for OnePlus 7T Pro.
The official 2026-10-16 build manifest pins kernel base
`0521dc291cf10bd754fb5ff385e74875c406d577`, identical to the previous LOS 23.2
kernel baseline. The KernelSU submodule is pinned to
`4c706b5938665866ebe16944a481a7b91e3396af` (33355).

The compatibility patch retains the v3.4.2 dual-policy SELinux context checks,
using native 4.14 policy locks, SID context hashing, and a separate snapshot
layout. It also preserves the module blacklist and shell_su_adb_only features.
SUSFS LKM sources are not enabled by this built-in port.

Successful full kernel build:
https://github.com/Gitawake/android_kernel_oneplus_sm8150_ksun/actions/runs/39036022443
Built commit: `b0ee6ef8a86d6ab3a4c602f4eeffc88b8b9a59b6`.

## Complete native-updater OTA

The local package workflow adds verified Android 17 MindTheGapps, the official
v3.4.2 standard manager, and Google-signed Gboard 18.4.1 base plus four splits
exported from this phone. APK signatures are preserved. Stock partition sizes
are sufficient; no repartitioning is performed. Linux tooling is needed to
mount offline ext4 copies and set UID/GID/modes/SELinux labels.

- `integration/integrate_gapps.py`: filesystem integration and addon.d manifest.
- `integration/normalize_boot_v2.py`: normalize the offset of an absent DTBO
  component so strict parsers accept the boot header; no component data moves.
- `integration/package_full_ota.sh`: rebuild/sign/verify with avbroot 3.35.0.
- `integration/updater-bootstrap/`: one-time KSU module for the original LOS 23
  Updater. It preserves the original OTA trust store, adds this package's public
  certificate, and enables `lineage.updater.allow_major_upgrades`. It uses an
  explicit bind mount, not a dependency on a specific metamodule.

The rootless avbroot flag skips Magisk injection only: the replacement boot
already contains KernelSU. Original top-level vbmeta disable flags are cleared
so the resulting custom AVB chain can be verified. This does not lock the
bootloader or provision a custom bootloader key.

Signing private keys remain only in the local `los24-20261016/signing-private`
directory with restricted permissions. They are not included in Git or release
files. Keep them backed up for future packages. Full ROM binaries are local
artifacts, not source files in this repository.

On 2026-10-17, hotdog / HD1911 was upgraded using the official recovery guide:
official LOS 24.0-20261016, then MindTheGapps 17 before the first Android boot.
The v3.4.2 kernel passed temporary boot testing, was flashed to the verified
current boot_a, and passed a normal reboot plus boot-image prefix readback.
Root, kernel interface 33355, manager/ksud 3.4.2, SELinux enforcing and a real
Wi-Fi connection with the stock WLAN module passed. Gboard remained the default.

This does not validate the custom complete OTA or native-updater upgrade path;
that package remains statically verified only. Third-party modules and the old
updater bootstrap remain disabled. The known stock charging IRQ warning is still
present; long-term stability, Warp charging and the old memcg issue remain
unresolved. Private backups and raw logs are local only, never uploaded here.
