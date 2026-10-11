# OnePlus 7T Pro / LOS 23.2 / KernelSU Next

Status: experimental source integration. Not compiled or device-tested yet.

LOS base: `0521dc291cf10bd754fb5ff385e74875c406d577` (lineage-23.2).
KernelSU Next legacy: `8869bd768d6650198810f2395c2762fabefc8557` (2026-10-06).
Latest upstream stable release observed on 2026-10-11: v3.4.1.

The legacy revision is the official old-kernel compatibility implementation,
NOT the v3.4.1 release tag. No version spoofing is applied. Compatibility with
the v3.4.1 official manager must be verified; the existing spoofed APK is not
assumed compatible.

Manual hooks are installed in exec, faccessat, newfstatat, read, reboot and
input_handle_event. UID and package tracking use the legacy driver's LSM hooks.
KernelSU is built into the kernel, not as a loadable GKI module.

The Actions workflow initially uses distro LLVM 18 for compile validation.
It must not be assumed identical to the toolchain of the installed LOS build.
The device configuration is sm8150-perf_defconfig + oplus.config + ksun.config.

Actions exports raw Image, DTBs, module metadata and available modules. These
are not yet a flashable boot image or AnyKernel ZIP. Packaging must preserve
the ramdisk from the exact target LOS boot, select the hotdog DTB and validate
WLAN module compatibility. No automatic installation or release publishing.

LOS OTA overwrites boot. Rebuild and install a compatible kernel for the new
LOS build; this repository alone does not preserve root across OTA.
