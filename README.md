# RFID Wisp

Desktop app for reading and writing the MIFARE Classic 1K RFID tags used by
QIDI's multi-color filament boxes, backed by
[Spoolman](https://github.com/Donkie/Spoolman) for spool/filament data and
[Moonraker](https://github.com/Arksine/moonraker) for live printer status.

This repository hosts only the built releases. Grab the executable for your
platform from the [Releases page](https://github.com/ThorSc/RFID-wisp/releases/latest) -
there is no source code here, and no installation is required.

## Downloads

Each release provides one executable per platform:

| Platform | File            |
|----------|-----------------|
| Windows  | `RFID-Wisp.exe` |
| Linux    | `RFID-Wisp-linux` |
| macOS    | `RFID-Wisp-macos` |

On Linux/macOS, mark the file executable before running it:

```sh
chmod +x RFID-Wisp-linux   # or RFID-Wisp-macos
./RFID-Wisp-linux
```

## Requirements

- A PC/SC-compatible RFID reader (e.g. an ACS ACR122), with its driver/PC/SC
  middleware installed:
  - **Windows** - PC/SC support (WinSCard) is built in.
  - **macOS** - PC/SC support is built in.
  - **Linux** - install and run `pcscd` (e.g. `sudo apt install pcscd` /
    `sudo systemctl enable --now pcscd`), plus your reader's CCID/ACS driver
    if it isn't already recognized by the generic CCID driver.
- A reachable [Spoolman](https://github.com/Donkie/Spoolman) instance.
- Optionally, a QIDI printer running Moonraker for live box/slot status.

## Configuration

On first run, the app creates a `config.ini` next to the executable holding
the Spoolman address, configured printers, and the standard RFID reader -
all of which can also be managed from the app's Settings panel.
