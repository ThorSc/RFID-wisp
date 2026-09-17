# Changelog

All notable changes to RFID Wisp are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.5.0] - 2026-09-17

### Added

- Generate a QR code for a spool's data (material, vendor, color, number)
  from the Spoolman Data panel, and save it as a print-ready 20x20mm PDF.
- QIDI Data now reads a slot's linked Spoolman spool number and vendor
  straight from the box's RFID data, instead of requiring manual entry.
- License information (`LICENSE`, `THIRD-PARTY-LICENSES.md`) for this
  release and the open-source libraries it uses.

### Changed

- Renamed "Manufacturer" to "Vendor" throughout the app.
- Cleaner, read-only QIDI Data fields that no longer look greyed-out or
  editable.

### Fixed

- The app no longer shows an error reading QIDI Data while a print is
  actively pulling filament from a slot.

## [0.4.0] - 2026-09-16

### Added

- Write RFID Tag dialog: pick an existing Spoolman filament directly
  (shown with its actual color) to prefill material, vendor,
  color and weight, instead of setting each field by hand.
- Initial weight / Remaining weight field: set the starting weight
  when creating a new spool, or see the spool's current remaining
  weight when writing an existing one.
- New "Use Spoolman" setting: turn it off to read/write tags with only
  the plain QIDI Box values, without a Spoolman server at all.
- The app now checks GitHub once on startup for a newer release and
  offers to open the download page - toggle it off in Settings if you
  don't want that.
- Writing a tag no longer closes the dialog, so a duplicate can be
  written to a second or third physical tag right away with the same
  values.

### Fixed

- Reading back a tag written for a spool with a linked Spoolman
  vendor no longer fails, and the material/color it shows now
  matches exactly what was written instead of being guessed from
  Spoolman's data.

## [0.3.0] - 2026-09-12

### Added

- `rfid_bridge` now automatically reports the active spool to
  Moonraker's built-in Spoolman integration (`/server/spoolman/spool_id`)
  whenever the RFID data for the active box slot changes or a print job
  starts, so Fluidd/Spoolman's active spool follows the box without
  manual selection. Verified against a live Moonraker/Fluidd/Spoolman
  stack.
- Tooltips on every interactive control across the app (Spool/QIDI Data,
  Settings, Actions, and the RFID tag read/write dialog) explaining
  what each field and button does.

## [0.2.1] - 2026-09-09

### Added

- Linux and macOS executables, built alongside the existing Windows
  `.exe` on every tagged release.

## [0.2.0] - 2026-09-09

### Added

- RFID tag writer dialog: create a new Spoolman spool or pick an
  existing one, then write its material/color/vendor/spool
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

[0.5.0]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.5.0
[0.4.0]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.4.0
[0.3.0]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.3.0
[0.2.1]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.2.1
[0.2.0]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.2.0
[0.1.0]: https://github.com/ThorSc/RFID-wisp/releases/tag/v0.1.0
