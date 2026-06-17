"""
estorides_core.transliteration
==============================
Cross-script name normalisation for entity resolution.

State-level person/organisation matching lives or dies on names that
arrive in different writing systems: a sanctions list spells a target in
Cyrillic, a leak spells him in Latin, a news article in Arabic. This
module folds all of them onto a single comparable Latin (ASCII) skeleton
so the resolver can score them against each other.

It is deliberately stdlib-only (no `unidecode`, no `transliterate`) so it
adds zero hard dependencies, consistent with the rest of the engine. The
maps are pragmatic romanisations (BGN/PCGN-leaning for Cyrillic/Greek,
ALA-LC-leaning for Arabic), not bit-exact standards; for fuzzy name
matching, recall matters more than scholarly fidelity.

Two representations are produced:

* ``to_latin(text)`` — best-effort Latin transliteration, lowercased and
  stripped of diacritics. ``"Владимир" -> "vladimir"``.
* ``consonant_skeleton(text)`` — the Latin form with vowels removed, so a
  vowelless Arabic spelling can still meet a fully-vowelled Latin one.
  Arabic script omits short vowels, so ``"محمد"`` romanises to ``"mhmd"``
  while the Latin source has ``"muhammad"``; comparing consonant
  skeletons (``"mhmd"`` vs ``"mhmd"``) recovers the match.
"""
from __future__ import annotations

import unicodedata
from typing import Dict

# --------------------------------------------------------------------------
# Per-script romanisation tables. Keys are single source characters; values
# are their Latin replacements (which may be multi-character, e.g. щ -> shch).
# --------------------------------------------------------------------------

_CYRILLIC: Dict[str, str] = {
    "а": "a", "б": "b", "в": "v", "г": "g", "ґ": "g", "д": "d", "е": "e",
    "ё": "e", "є": "ye", "ж": "zh", "з": "z", "и": "i", "і": "i", "ї": "yi",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
    "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "", "э": "e",
    "ю": "yu", "я": "ya", "ђ": "dj", "ј": "j", "љ": "lj", "њ": "nj",
    "ћ": "c", "џ": "dz",
}

_GREEK: Dict[str, str] = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "i",
    "θ": "th", "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "x",
    "ο": "o", "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t", "υ": "y",
    "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
}

_ARABIC: Dict[str, str] = {
    "ا": "a", "أ": "a", "إ": "i", "آ": "a", "ب": "b", "ت": "t", "ث": "th",
    "ج": "j", "ح": "h", "خ": "kh", "د": "d", "ذ": "dh", "ر": "r", "ز": "z",
    "س": "s", "ش": "sh", "ص": "s", "ض": "d", "ط": "t", "ظ": "z", "ع": "a",
    "غ": "gh", "ف": "f", "ق": "q", "ك": "k", "ل": "l", "م": "m", "ن": "n",
    "ه": "h", "و": "w", "ي": "y", "ى": "a", "ء": "", "ؤ": "w", "ئ": "y",
    "ة": "h", "پ": "p", "چ": "ch", "ژ": "zh", "گ": "g", "ک": "k", "ی": "y",
    # Arabic-Indic and Eastern Arabic-Indic digits.
    "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4", "٥": "5", "٦": "6",
    "٧": "7", "٨": "8", "٩": "9", "۰": "0", "۱": "1", "۲": "2", "۳": "3",
    "۴": "4", "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9",
}

# Merge into one lookup. Disjoint code points, so a flat dict is safe.
_CHAR_MAP: Dict[str, str] = {}
for _table in (_CYRILLIC, _GREEK, _ARABIC):
    _CHAR_MAP.update(_table)

_LATIN_VOWELS = frozenset("aeiou")


def _strip_diacritics(text: str) -> str:
    """Drop combining marks via NFKD decomposition.

    Folds ``é`` -> ``e``, ``ü`` -> ``u``, full-width forms to ASCII, and so
    on. Characters that have no compatibility decomposition pass through
    unchanged and are handled by the per-script map instead.
    """
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def to_latin(text: str) -> str:
    """Return a lowercased, diacritic-free Latin transliteration.

    The pipeline is: casefold -> NFKD diacritic strip (so accented Greek
    and Latin fold to their base letters) -> per-character script map
    (Cyrillic/Greek/Arabic) -> keep only ``[a-z0-9 ]``. Casefolding and
    stripping run *before* the map so that uppercase and accented source
    letters reach the lowercase, accent-free keys the map is written for.
    Whitespace is collapsed to single spaces and the result is trimmed.
    Non-mappable characters (e.g. unmapped CJK) are dropped, which is the
    safe failure mode for fuzzy matching.
    """
    if not text:
        return ""
    folded = _strip_diacritics(text.casefold())
    mapped = "".join(_CHAR_MAP.get(ch, ch) for ch in folded)
    out_chars = []
    for ch in mapped:
        if ch.isalnum() and ch.isascii():
            out_chars.append(ch)
        elif ch.isspace():
            out_chars.append(" ")
    return " ".join("".join(out_chars).split())


def consonant_skeleton(text: str) -> str:
    """Return the Latin transliteration with vowels and spaces removed.

    This is the vowel-insensitive comparison key. Abjad scripts (Arabic,
    Hebrew) routinely omit short vowels, so two spellings of the same name
    can only be reconciled on their consonant skeletons. The first
    character is preserved even if it is a vowel, because name-initial
    vowels are usually written and carry signal.

    Adjacent duplicate letters are collapsed so that gemination written as
    a doubled Latin consonant (``Muhammad`` -> ``mhmmd``) reconciles with a
    script that marks it with a diacritic instead of doubling the letter
    (Arabic ``محمد`` -> ``mhmd``).
    """
    latin = to_latin(text).replace(" ", "")
    if not latin:
        return ""
    head = latin[0]
    tail = "".join(ch for ch in latin[1:] if ch not in _LATIN_VOWELS)
    skeleton = head + tail
    collapsed = [skeleton[0]]
    for ch in skeleton[1:]:
        if ch != collapsed[-1]:
            collapsed.append(ch)
    return "".join(collapsed)


def is_non_latin(text: str) -> bool:
    """True if any character is outside the Basic Latin / Latin-1 range.

    Used by the resolver to decide whether the cross-script path is worth
    taking for a given value before paying for transliteration of both
    sides of a comparison.
    """
    return any(ord(ch) > 0x024F for ch in text)
