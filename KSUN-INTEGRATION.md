# LOS 23.2 / hotdog / KernelSU Next v3.4.1 port

Experimental work in progress. Do not flash until boot and WLAN validation complete.

Kernel base: LineageOS lineage-23.2, 0521dc291cf10bd754fb5ff385e74875c406d577.
KernelSU Next: official release v3.4.1, 8f902aeb16033024143ae36cf711df902cf02fae.
The submodule stays pinned to the release; Actions applies the tracked compatibility patch.
This is a port of the release kernel code, not the legacy branch or a spoofed version.

The initial adaptation preserves the native six-argument ARM64 syscall ABI used
by this 4.14 kernel. It adapts the dispatcher, direct boot-time read/fstat hooks,
original syscall invocation, and reboot kprobe register handling.
Further API compatibility changes will be driven by compilation and review.

Raw Image and matching WLAN modules are experimental outputs; packaging and
on-device validation are pending. The separate los-23.2-ksun branch is the earlier
legacy reference build and does not satisfy the v3.4.1 target.

## Compatibility work

The release code now has adapters for native ARM64 syscalls, nofault user/kernel
copies, task-work notification, old seccomp state, mount namespace operations,
block page-table mappings, filesystem notification, and file-operation wrappers.
The SELinux adapter keeps the release's copy/edit/publish transaction. It uses a
port-owned snapshot instead of casting the older selinux_ss structure, publishes
under its reader/writer lock, and serializes with native policy loading and boolean
writes through a mutex. Policy backups own a separate class map. Linux 4.14 flex
arrays and filename transition tables have dedicated adapters; newer code paths
are retained. These adaptations still need runtime validation.

## Matching stock boot

The verified stock payload is lineage-23.2-20260925-nightly-hotdog-signed.zip.
Its boot SHA-256 is
4368d800dcdd85f4601ca197508d6eff5fb50ca4cab36723da9336f79bf2a39c.
Its embedded kernel identifies the same LOS source commit, 0521dc291cf1,
and Android clang r563880c (21.0.0). Current CI uses Ubuntu clang 18;
compiler/configuration compatibility remains part of validation.

`integration/extract_los_boot.py` verifies operation and partition hashes from a
full OTA payload. `integration/repack_los_boot.py` uses AOSP mkbootimg/unpack_bootimg
and preserves stock ramdisk, DTB, and boot header parameters. Obtain those tools
from https://android.googlesource.com/platform/system/tools/mkbootimg at
 d2bb0af5ba6d3198a3e99529c97eda1be0b5a093 and pass their path with `--tools`.
The repacker creates an unsigned image, discards the stale original AVB footer,
checks partition size, and verifies the repacked components. A stock round trip
has passed; this does not validate a custom kernel on the device.

WLAN is a loadable qca_cld3_wlan.ko under /vendor_dlkm/lib/modules. Ship and verify
the module from the same build, together with boot. Existing crDroid replacement
modules must not be mistaken for LOS modules. No device partitions have been
written during this port.
