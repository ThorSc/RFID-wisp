# RFID bridge for the QIDI multi-color box.
#
# Captures the raw 16-byte fm17550_read_card_return payload per box slot,
# correlated with the slot that was active when it arrived, without
# touching any QIDI-shipped file on disk (mcu.py, stepper_enable.py,
# box_rfid.so, box_stepper.so).
#
# How it works:
#   - stepper_enable's EnableTracking.register_state_callback() (public
#     Klipper API) tells us which "box_stepper slotN" is currently active,
#     tracked purely in memory (no /tmp files).
#   - CommandQueryWrapper.send() in klippy's own mcu.py is monkey-patched
#     at runtime (in-memory only, mcu.py on disk is never modified) to
#     intercept every "fm17550_read_card_return" response - the same
#     response QIDI's own box_rfid code consumes to populate
#     multi_color_controller. We only observe it; we never touch the
#     handler QIDI itself registered, so their own read logic is
#     unaffected.
#
# Confirmed byte layout (matches multi_color_controller.config exactly):
#   data[0] = filament_type_id, data[1] = color_id, data[2..] = 0 (QIDI
#   only ever writes/uses the first ~3 bytes). Bytes 3-15 are free for
#   custom use (e.g. a Spoolman spool id + weight written externally).
#
# printer.cfg:
#   [rfid_bridge]
#   box_stepper_count: 4
#
# Query via Moonraker: GET /printer/objects/query?rfid_bridge
# Or:  RFID_BRIDGE_STATUS

import logging

import mcu as mcu_module


class RFIDBridge:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.slot_count = config.getint('box_stepper_count', 4)

        self.current_slot = None       # int or None
        self.last_raw = {}             # slot(int) -> bytes(16)
        self.last_raw_time = {}        # slot(int) -> reactor monotonic time
        self._pending_slots = set(range(self.slot_count))
        self._registered_slots = set()

        self._patch_mcu_send()
        self.printer.register_event_handler("klippy:connect", self._connect)

        gcode = self.printer.lookup_object('gcode')
        gcode.register_command(
            "RFID_BRIDGE_STATUS", self.cmd_RFID_BRIDGE_STATUS,
            desc=self.cmd_RFID_BRIDGE_STATUS_help)

    def _patch_mcu_send(self):
        cls = mcu_module.CommandQueryWrapper
        if getattr(cls, '_rfid_bridge_orig_send', None) is not None:
            return  # already patched (e.g. by a prior [rfid_bridge] load)
        orig_send = cls.send
        bridge = self

        def patched_send(wrapper_self, data=(), minclock=0, reqclock=0):
            resp = orig_send(wrapper_self, data, minclock, reqclock)
            try:
                if (wrapper_self._response == "fm17550_read_card_return"
                        and isinstance(resp, dict)
                        and resp.get("status") == 1):
                    bridge._handle_raw_read(resp.get("data"))
            except Exception:
                logging.exception("rfid_bridge: error handling RFID response")
            return resp

        cls._rfid_bridge_orig_send = orig_send
        cls.send = patched_send

    def _handle_raw_read(self, data):
        if self.current_slot is None or data is None:
            return
        raw = bytes(data)
        self.last_raw[self.current_slot] = raw
        self.last_raw_time[self.current_slot] = (
            self.printer.get_reactor().monotonic())
        logging.info("rfid_bridge: slot%d raw=%s",
                     self.current_slot, raw.hex())

    def _connect(self):
        """Track which box_stepper slot is active (public callback API).

        The box hardware finishes its own init/handshake some time after
        Klipper starts, so "box_stepper slotN" objects may not exist yet
        at klippy:connect. Keep retrying until all slots are found (or
        forever, at a low rate - harmless if some slots never appear).
        """
        reactor = self.printer.get_reactor()
        reactor.register_timer(self._try_register_slots, reactor.NOW)

    def _try_register_slots(self, eventtime):
        stepper_enable = self.printer.lookup_object('stepper_enable')
        for slot in list(self._pending_slots):
            name = "box_stepper slot%d" % slot
            try:
                enable = stepper_enable.lookup_enable(name)
            except Exception:
                continue
            enable.register_state_callback(self._make_callback(slot))
            self._pending_slots.discard(slot)
            self._registered_slots.add(slot)
            logging.info("rfid_bridge: registered '%s'", name)
        if not self._pending_slots:
            return self.printer.get_reactor().NEVER
        return eventtime + 2.0

    def _make_callback(self, slot):
        def callback(print_time, is_enable):
            if is_enable:
                self.current_slot = slot
        return callback

    cmd_RFID_BRIDGE_STATUS_help = (
        "Show the last raw fm17550 RFID payload captured per box slot")

    def cmd_RFID_BRIDGE_STATUS(self, gcmd):
        if not self.last_raw:
            gcmd.respond_info("RFID_BRIDGE_STATUS: no data captured yet")
            return
        for slot in sorted(self.last_raw):
            gcmd.respond_info(
                "slot%d: %s" % (slot, self.last_raw[slot].hex()))

    def get_status(self, eventtime):
        return {
            "current_slot": self.current_slot,
            "registered_slots": sorted(self._registered_slots),
            "pending_slots": sorted(self._pending_slots),
            "last_raw": {
                "slot%d" % slot: data.hex()
                for slot, data in self.last_raw.items()
            },
            "last_raw_time": {
                "slot%d" % slot: t
                for slot, t in self.last_raw_time.items()
            },
        }


def load_config(config):
    return RFIDBridge(config)
