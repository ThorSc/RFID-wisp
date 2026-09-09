# Changelog

All notable changes to RFID Wisp are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.1] - 2026-09-09

### Added

- Linux and macOS executables, built alongside the existing Windows
  `.exe` on every tagged release.

## [0.2.0] - 2026-09-09

### Added

- RFID tag writer dialog: create a new Spoolman spool or pick an
  existing one, then write its material/color/manufacturer/spool
  number to a tag.
- Capability-based reader filtering: only readers proven to support
  MIFARE Classic 1K tags are offered, instead of relying on reader
  names.
- Standard reader setting that auto-connects on startup.

## [0.1.0] - 2026-09-08

### Added

- Initial release: read/write MIFARE Classic 1K RFID tags for QIDI
  multi-color filament boxes.
- Spoolman integration for spool/filament data.
- Moonraker integration showing live QIDI box/slot status.
- Klipper `rfid_bridge` companion module capturing raw RFID payloads
  during printing.
- Automated Windows `.exe` release pipeline.

[0.2.1]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.2.1
[0.2.0]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.2.0
[0.1.0]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.1.0
