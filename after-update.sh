#!/bin/sh
# Run by hermes-patches.service after the Hermes checkout moves (hermes update):
# diff the Thai pack against the new English and pop a desktop notification if it needs work.
TOOLS="$HOME/.hermes/plugins/hermes-lang-th/tools"
LOG="$TOOLS/after-update.log"
export DISPLAY="${DISPLAY:-:0}" DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=/run/user/$(id -u)/bus}"

cd "$TOOLS" || exit 0
date >> "$LOG"
if ! out=$(python3 langpack.py export 2>&1 && python3 langpack.py diff 2>&1); then
    echo "$out" >> "$LOG"
    notify-send -a Hermes -u critical "Thai pack check failed" "export/diff failed after hermes update, see $LOG"
    exit 0
fi
echo "$out" | tail -2 >> "$LOG"
todo=$(echo "$out" | sed -n 's/^to translate: \([0-9]*\) keys.*/\1/p')
removed=$(echo "$out" | sed -n 's/.*removed from English: \([0-9]*\).*/\1/p')
if [ "${todo:-0}" -gt 0 ] || [ "${removed:-0}" -gt 0 ]; then
    notify-send -a Hermes "Hermes updated, Thai pack is behind" \
        "New/changed: ${todo:-0}, removed: ${removed:-0}. Ask Hermes to update the Thai pack."
fi
