import pathlib
import json

PREF_KEYS = ["shorten_utun", "shorten_en"]


class Prefs:
    _pref_file = pathlib.Path.home() / ".netivity"

    def write_pref(self, key, value):
        self.prefs[key] = value
        self._pref_file.write_text(json.dumps(self.prefs))

    def apply_prefs(self, app):
        app.menu["Settings"]["Shorten `utun` to `t` in the menu bar"].state = (
            self.prefs["shorten_utun"]
        )
        app.menu["Settings"]["Shorten `en` to `e` in the menu bar"].state = self.prefs[
            "shorten_en"
        ]

    def load_prefs(self):
        if not self._pref_file.exists():
            self._pref_file.write_text(
                json.dumps({"shorten_utun": False, "shorten_en": False})
            )
        prefs_raw = self._pref_file.read_text()
        prefs = json.loads(prefs_raw)
        for key in PREF_KEYS:
            if key not in prefs:
                prefs[key] = False

        self.prefs = prefs
