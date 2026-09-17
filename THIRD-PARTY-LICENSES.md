# Third-Party Licenses

RFID Wisp is licensed under the MIT License (see [LICENSE](LICENSE)). It
depends on the third-party open-source packages listed below, each under its
own license. This file exists so that redistributing RFID Wisp - as source,
as a `pip install`, or as a packaged executable built with PyInstaller -
comes with the attribution and license texts those packages require.

Full, verbatim license texts are kept in [`THIRD-PARTY-LICENSES/`](THIRD-PARTY-LICENSES/),
one file per package, copied unmodified from the package as published. This
document is a summary and index into that folder, not a substitute for it -
when in doubt, the files in that folder are authoritative.

## Summary table

| Package | Version | License | Copyright | License text |
|---|---|---|---|---|
| [requests](https://github.com/psf/requests) | 2.34.2 | Apache-2.0 | 2019 Kenneth Reitz | [requests-2.34.2-Apache-2.0.txt](THIRD-PARTY-LICENSES/requests-2.34.2-Apache-2.0.txt), [NOTICE](THIRD-PARTY-LICENSES/requests-2.34.2-NOTICE.txt) |
| [certifi](https://github.com/certifi/python-certifi) | 2026.7.22 | MPL-2.0 | Kenneth Reitz | [certifi-2026.7.22-MPL-2.0.txt](THIRD-PARTY-LICENSES/certifi-2026.7.22-MPL-2.0.txt) |
| [charset-normalizer](https://github.com/jawah/charset_normalizer) | 3.5.1 | MIT | Ahmed TAHRI | [charset-normalizer-3.5.1-MIT.txt](THIRD-PARTY-LICENSES/charset-normalizer-3.5.1-MIT.txt) |
| [idna](https://github.com/kjd/idna) | 3.19 | BSD-3-Clause | Kim Davies | [idna-3.19-BSD-3-Clause.txt](THIRD-PARTY-LICENSES/idna-3.19-BSD-3-Clause.txt) |
| [urllib3](https://github.com/urllib3/urllib3) | 2.7.0 | MIT | Andrey Petrov | [urllib3-2.7.0-MIT.txt](THIRD-PARTY-LICENSES/urllib3-2.7.0-MIT.txt) |
| [pyscard](https://github.com/LudovicRousseau/pyscard) | 2.3.1 | LGPL-2.1-or-later | Ludovic Rousseau | [pyscard-2.3.1-LGPL-2.1.txt](THIRD-PARTY-LICENSES/pyscard-2.3.1-LGPL-2.1.txt) |
| [qrcode](https://github.com/lincolnloop/python-qrcode) | 8.2 | BSD-3-Clause | 2011 Lincoln Loop | [qrcode-8.2-BSD-3-Clause.txt](THIRD-PARTY-LICENSES/qrcode-8.2-BSD-3-Clause.txt) |
| [colorama](https://github.com/tartley/colorama) | 0.4.6 | BSD-3-Clause | 2010 Jonathan Hartley | [colorama-0.4.6-BSD-3-Clause.txt](THIRD-PARTY-LICENSES/colorama-0.4.6-BSD-3-Clause.txt) |
| [Pillow](https://python-pillow.org/) | 12.3.0 | MIT-CMU | Secret Labs AB / Jeffrey A. Clark and contributors | [Pillow-12.3.0-MIT-CMU-and-bundled-components.txt](THIRD-PARTY-LICENSES/Pillow-12.3.0-MIT-CMU-and-bundled-components.txt) |

`certifi`, `charset-normalizer`, `idna`, `urllib3` and `colorama` are not
imported directly by RFID Wisp's own code - they are dependencies pulled in
by `requests` and `qrcode` respectively, and end up bundled in any packaged
build the same way. `pytest` (used only for the test suite) is a
development-only dependency and is never bundled into a distributed build,
so it is not listed here.

## Where each package is used

- **requests** - Moonraker and Spoolman HTTP API clients, and the GitHub
  release check (`src/moonraker_api.py`, `src/spoolman_api.py`,
  `src/update_checker.py`).
- **pyscard** - PC/SC smart card reader access (`src/UI/rfid_reader.py`).
- **qrcode** / **Pillow** - QR code generation and PDF export for a spool's
  data (`src/UI/qr_code_window.py`).

## Notes on license compatibility

All of the above are permissive open-source licenses. None of them is
copyleft in a way that would require RFID Wisp itself to be open-sourced,
and none of them conflicts with RFID Wisp's own MIT license. Two are worth
calling out specifically:

- **pyscard is LGPL-2.1-or-later.** Unlike the MIT/BSD-style licenses here,
  the LGPL does impose real obligations when distributing a binary build
  (e.g. the PyInstaller executables published in GitHub releases):
  - Include a copy of the LGPL-2.1 license text (done - see
    [pyscard-2.3.1-LGPL-2.1.txt](THIRD-PARTY-LICENSES/pyscard-2.3.1-LGPL-2.1.txt)).
  - Give clear notice that pyscard is used, under LGPL-2.1-or-later, and
    point to its source (this file, plus the upstream repository linked in
    the table above).
  - Don't modify pyscard's own source before redistributing it; if it is
    ever patched, the corresponding source changes would need to be made
    available under the LGPL as well.
  - The LGPL also expects that a user can relink/replace the LGPL component
    with a modified version. Build RFID Wisp's executable with PyInstaller's
    `--onedir` mode (rather than `--onefile`) if this matters for a given
    release, since it keeps pyscard's compiled extension as a separate,
    swappable file instead of folding it into a single compressed binary.
  - This is general information, not legal advice - for a distribution
    model with stricter compliance needs, have this reviewed by a lawyer.
- **certifi is MPL-2.0**, a weak (file-level) copyleft license. It only
  requires source disclosure for files from certifi itself that are
  *modified* before redistribution. RFID Wisp uses certifi unmodified as an
  ordinary dependency, so the only practical obligation is including its
  license text (done above).

## Pillow's bundled binary components

Pillow's published wheels statically include several third-party C
libraries (image/font codecs) so that Pillow works without separate system
installs. Their license notices are aggregated, unmodified, in
[Pillow-12.3.0-MIT-CMU-and-bundled-components.txt](THIRD-PARTY-LICENSES/Pillow-12.3.0-MIT-CMU-and-bundled-components.txt),
exactly as Pillow itself ships them. All of them are permissive
(BSD-style, MIT-style, or zlib-style) - none is copyleft:

brotli, FreeType, harfbuzz, Little CMS (lcms2), libavif, libjpeg-turbo,
libpng, libwebp, OpenJPEG, libtiff, xz, zlib-ng.

## Keeping this up to date

If a dependency in `requirements.txt` is added, removed, or has its version
bumped, refresh this file and the `THIRD-PARTY-LICENSES/` folder to match
(`pip show <package>` for the license/author, and the package's
`*.dist-info/licenses/` folder - or `*.dist-info/LICENSE*` on older
packaging metadata - inside the virtualenv for the exact text).
