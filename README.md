# RFID Wisp

A cross-platform desktop app for reading and writing the MIFARE Classic 1K
RFID tags used by QIDI's multi-color filament boxes, backed by
[Spoolman](https://github.com/Donkie/Spoolman) for spool/filament data and
[Moonraker](https://github.com/Arksine/moonraker) for live printer status.

This repository hosts only the built releases; there is no source code here
and no installation is required.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## Downloads

Each release provides one executable per platform - grab yours from the
[Releases page](https://github.com/ThorSc/RFID-wisp/releases/latest):

| Platform | File | Notes |
|----------|------|-------|
| Windows  | `RFID-Wisp.exe`   | Run directly. |
| Linux    | `RFID-Wisp-linux` | `chmod +x RFID-Wisp-linux` first. |
| macOS    | `RFID-Wisp-macos` | `chmod +x RFID-Wisp-macos` first. |

## Features

- Connects to any PC/SC-compatible RFID reader (tested with the ACS ACR122)
  and probes each reader's real capability instead of trusting its reported
  name, so only readers that actually work with MIFARE Classic 1K tags
  are offered.
- Reads and dumps the full 16-sector/64-block memory layout of a tag for
  inspection.
- Writes filament metadata (material, color, manufacturer, spool number) to a
  tag, either for a new Spoolman spool (created on the fly) or an existing
  one picked from Spoolman.
- Shows the four material slots of one or more QIDI boxes live via Moonraker,
  including the last recorded remaining weight from Spoolman.
- Manages multiple printers and a Spoolman server address from a settings
  panel, persisted to `config.ini`.

## Requirements

- A PC/SC-compatible RFID reader (tested with the ACS ACR122), with its
  driver/PC/SC middleware installed:
  - **Windows** - PC/SC support (WinSCard) is built in.
  - **macOS** - PC/SC support is built in.
  - **Linux** - install and run `pcscd` (e.g. `sudo apt install pcscd` /
    `sudo systemctl enable --now pcscd`), plus your reader's CCID/ACS driver
    if it isn't already recognized by the generic CCID driver.
- A reachable [Spoolman](https://github.com/Donkie/Spoolman) instance.
- Optionally, a QIDI printer running Moonraker for live box/slot status.

## Configuration

On first run, the app creates a `config.ini` next to the executable. It can
be edited directly, or entirely from the app's Settings panel:

```ini
[spoolman]
base_url = http://<spoolman-host>:7912

[printer:printer1]
name = My Printer
address = http://<printer-host>:7125

[reader]
standard = <PC/SC reader name>
```

## Usage

1. Start the app and expand **Settings**.
2. Pick an RFID reader from the list (only readers that pass a non-destructive
   RFID capability probe are shown) and click **Connect**, or mark one
   reader as the standard reader to have it auto-connect on startup.
3. Add your printer's Moonraker address and your Spoolman server address.
4. The spool panel shows the loaded QIDI box(es) and their four material
   slots, refreshed from Moonraker.
5. Click **Write Tag** to open the tag-writing dialog: pick an existing
   Spoolman spool or create a new one, choose material/manufacturer/color,
   place a blank tag on the reader, and write it to a sector (sector 1 by
   default, matching the QIDI box read location).

## Klipper integration (`rfid_bridge`)

To have your QIDI printer capture the raw RFID payload of each loaded spool
during printing (so it can be correlated with the tag data written above),
install [`rfid_bridge.py`](rfid_bridge.py) as a Klipper extra:

1. Download [`rfid_bridge.py`](https://github.com/ThorSc/RFID-wisp/raw/main/rfid_bridge.py)
   and copy it into Klipper's `klippy/extras/` directory on the printer.
2. Add to `printer.cfg`:

   ```ini
   [rfid_bridge]
   box_stepper_count: 4
   ```

3. Restart Klipper (`RESTART` or `FIRMWARE_RESTART`).

It works by capturing the raw 16-byte `fm17550_read_card_return` response
QIDI's own firmware already reads for each box slot - the same data the
box uses internally - without modifying any QIDI-shipped file on disk. The
patch is purely observational and is automatically undone by any Klipper
restart.

Query the captured data via `RFID_BRIDGE_STATUS` in the Klipper console, or
`GET /printer/objects/query?rfid_bridge` through Moonraker.
