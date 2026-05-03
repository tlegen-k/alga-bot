from bot.i18n import kk, ru, en

_langs = {"kk": kk.strings, "ru": ru.strings, "en": en.strings}


def get_text(key: str, lang: str = "kk") -> str:
    return _langs.get(lang, _langs["kk"]).get(key) or _langs["kk"][key]
