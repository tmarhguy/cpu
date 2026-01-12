# Release build notes

This document describes how to prepare a release package for the CPU project.

## Package contents

Package the following artifacts into a single release bundle (for example, a ZIP
or tarball). Use a top-level directory named `cpu-<version>/` so the release
can be unpacked cleanly.

### Schematics

1. Export the latest schematics from KiCad as PDF.
2. Include the KiCad source files for the released revision.
3. Record the exact KiCad version used to export the PDFs.

Suggested paths in the bundle:

- `schematics/CPU.pdf`
- `schematics/kicad/` (project sources)
- `schematics/README.txt` (KiCad version and notes)

### Firmware

1. Build the firmware from the tagged commit.
2. Include compiled binaries (HEX/ELF/ROM image as applicable).
3. Include the build command or script used to generate the binaries.

Suggested paths in the bundle:

- `firmware/` (binaries)
- `firmware/build-command.txt`
- `firmware/README.txt` (toolchain version, build notes)

### Test vectors

1. Export the golden test vectors used for verification.
2. Include any scripts needed to replay the vectors.
3. Record the generator version or commit hash.

Suggested paths in the bundle:

- `test-vectors/` (vector files)
- `test-vectors/run.sh` (or equivalent)
- `test-vectors/README.txt` (generation details)

## Release checklist

Use this checklist for every release:

- [ ] Confirm the release version number using `v<MAJOR>.<MINOR>.<PATCH>`.
- [ ] Update the changelog to include the release notes.
- [ ] Export schematics PDFs and include KiCad project sources.
- [ ] Build firmware and record toolchain/build commands.
- [ ] Export test vectors and note generator version/commit.
- [ ] Assemble the release bundle with the paths listed above.
- [ ] Verify the bundle contents match the checklist.
- [ ] Tag the release once all artifacts are complete and verified.

## Version numbering

The release version follows semantic versioning:

- **MAJOR**: hardware or interface changes that break compatibility.
- **MINOR**: new features or additions that remain compatible.
- **PATCH**: fixes, documentation updates, or non-breaking improvements.
