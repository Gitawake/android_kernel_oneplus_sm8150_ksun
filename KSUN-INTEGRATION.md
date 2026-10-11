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
