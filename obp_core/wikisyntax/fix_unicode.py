# Define the translation table.  I needed to hammer unicode going to
# NCBI's web services (for Biopython's EUtils package) so I used the
# table defined at
#  http://www.nlm.nih.gov/databases/dtd/medline_character_database.utf8
# This is not as extensive as the original conversion set.
class XLate(dict):
    def __getitem__(self, c):
        try:
            return dict.__getitem__(self, c)
        except KeyError:
            self[c] = None
            return None


# Convert these unicode characters into ASCII
xlate = XLate(
    {
        # The note at the bottom of the page says "the inverted question
        # mark represents a questionable character found as a result of
        # NLM's conversion from its legacy extended EBCDIC character set
        # to UNICODE UTF-8."  I do not use it but leave it here for
        # completeness.
        ord("\N{INVERTED QUESTION MARK}"): None,
        ord("\N{LATIN CAPITAL LETTER O WITH STROKE}"): "O",
        ord("\N{LATIN SMALL LETTER A WITH GRAVE}"): "a",
        ord("\N{LATIN SMALL LETTER A WITH ACUTE}"): "a",
        ord("\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}"): "a",
        ord("\N{LATIN SMALL LETTER A WITH TILDE}"): "a",
        ord("\N{LATIN SMALL LETTER A WITH DIAERESIS}"): "a",
        ord("\N{LATIN SMALL LETTER A WITH RING ABOVE}"): "a",
        ord("\N{LATIN SMALL LETTER C WITH CEDILLA}"): "c",
        ord("\N{LATIN SMALL LETTER E WITH GRAVE}"): "e",
        ord("\N{LATIN SMALL LETTER E WITH ACUTE}"): "e",
        ord("\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}"): "e",
        ord("\N{LATIN SMALL LETTER E WITH DIAERESIS}"): "e",
        ord("\N{LATIN SMALL LETTER I WITH GRAVE}"): "i",
        ord("\N{LATIN SMALL LETTER I WITH ACUTE}"): "i",
        ord("\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}"): "i",
        ord("\N{LATIN SMALL LETTER I WITH DIAERESIS}"): "i",
        ord("\N{LATIN SMALL LETTER N WITH TILDE}"): "n",
        ord("\N{LATIN SMALL LETTER O WITH GRAVE}"): "o",
        ord("\N{LATIN SMALL LETTER O WITH ACUTE}"): "o",
        ord("\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}"): "o",
        ord("\N{LATIN SMALL LETTER O WITH TILDE}"): "o",
        ord("\N{LATIN SMALL LETTER O WITH DIAERESIS}"): "o",
        ord("\N{LATIN SMALL LETTER O WITH STROKE}"): "o",
        ord("\N{LATIN SMALL LETTER U WITH GRAVE}"): "u",
        ord("\N{LATIN SMALL LETTER U WITH ACUTE}"): "u",
        ord("\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}"): "u",
        ord("\N{LATIN SMALL LETTER U WITH DIAERESIS}"): "u",
        ord("\N{LATIN SMALL LETTER Y WITH ACUTE}"): "y",
        ord("\N{LATIN SMALL LETTER Y WITH DIAERESIS}"): "y",
        ord("\N{LATIN SMALL LETTER A WITH MACRON}"): "a",
        ord("\N{LATIN SMALL LETTER A WITH BREVE}"): "a",
        ord("\N{LATIN SMALL LETTER C WITH ACUTE}"): "c",
        ord("\N{LATIN SMALL LETTER C WITH CIRCUMFLEX}"): "c",
        ord("\N{LATIN SMALL LETTER E WITH MACRON}"): "e",
        ord("\N{LATIN SMALL LETTER E WITH BREVE}"): "e",
        ord("\N{LATIN SMALL LETTER G WITH CIRCUMFLEX}"): "g",
        ord("\N{LATIN SMALL LETTER G WITH BREVE}"): "g",
        ord("\N{LATIN SMALL LETTER G WITH CEDILLA}"): "g",
        ord("\N{LATIN SMALL LETTER H WITH CIRCUMFLEX}"): "h",
        ord("\N{LATIN SMALL LETTER I WITH TILDE}"): "i",
        ord("\N{LATIN SMALL LETTER I WITH MACRON}"): "i",
        ord("\N{LATIN SMALL LETTER I WITH BREVE}"): "i",
        ord("\N{LATIN SMALL LETTER J WITH CIRCUMFLEX}"): "j",
        ord("\N{LATIN SMALL LETTER K WITH CEDILLA}"): "k",
        ord("\N{LATIN SMALL LETTER L WITH ACUTE}"): "l",
        ord("\N{LATIN SMALL LETTER L WITH CEDILLA}"): "l",
        ord("\N{LATIN CAPITAL LETTER L WITH STROKE}"): "L",
        ord("\N{LATIN SMALL LETTER L WITH STROKE}"): "l",
        ord("\N{LATIN SMALL LETTER N WITH ACUTE}"): "n",
        ord("\N{LATIN SMALL LETTER N WITH CEDILLA}"): "n",
        ord("\N{LATIN SMALL LETTER O WITH MACRON}"): "o",
        ord("\N{LATIN SMALL LETTER O WITH BREVE}"): "o",
        ord("\N{LATIN SMALL LETTER R WITH ACUTE}"): "r",
        ord("\N{LATIN SMALL LETTER R WITH CEDILLA}"): "r",
        ord("\N{LATIN SMALL LETTER S WITH ACUTE}"): "s",
        ord("\N{LATIN SMALL LETTER S WITH CIRCUMFLEX}"): "s",
        ord("\N{LATIN SMALL LETTER S WITH CEDILLA}"): "s",
        ord("\N{LATIN SMALL LETTER T WITH CEDILLA}"): "t",
        ord("\N{LATIN SMALL LETTER U WITH TILDE}"): "u",
        ord("\N{LATIN SMALL LETTER U WITH MACRON}"): "u",
        ord("\N{LATIN SMALL LETTER U WITH BREVE}"): "u",
        ord("\N{LATIN SMALL LETTER U WITH RING ABOVE}"): "u",
        ord("\N{LATIN SMALL LETTER W WITH CIRCUMFLEX}"): "w",
        ord("\N{LATIN SMALL LETTER Y WITH CIRCUMFLEX}"): "y",
        ord("\N{LATIN SMALL LETTER Z WITH ACUTE}"): "z",
        ord("\N{LATIN SMALL LETTER W WITH GRAVE}"): "w",
        ord("\N{LATIN SMALL LETTER W WITH ACUTE}"): "w",
        ord("\N{LATIN SMALL LETTER W WITH DIAERESIS}"): "w",
        ord("\N{LATIN SMALL LETTER Y WITH GRAVE}"): "y",
    }
)

# These are the ASCII characters NCBI knows about.  Note that I'm
# building one unicode string here, and not a tuple of unicode
# characters.
for c in (
    "\N{SPACE}"
    "\N{EXCLAMATION MARK}"
    "\N{QUOTATION MARK}"
    "\N{NUMBER SIGN}"
    "\N{DOLLAR SIGN}"
    "\N{PERCENT SIGN}"
    "\N{AMPERSAND}"
    "\N{APOSTROPHE}"
    "\N{LEFT PARENTHESIS}"
    "\N{RIGHT PARENTHESIS}"
    "\N{ASTERISK}"
    "\N{PLUS SIGN}"
    "\N{COMMA}"
    "\N{HYPHEN-MINUS}"
    "\N{FULL STOP}"
    "\N{SOLIDUS}"
    "\N{DIGIT ZERO}"
    "\N{DIGIT ONE}"
    "\N{DIGIT TWO}"
    "\N{DIGIT THREE}"
    "\N{DIGIT FOUR}"
    "\N{DIGIT FIVE}"
    "\N{DIGIT SIX}"
    "\N{DIGIT SEVEN}"
    "\N{DIGIT EIGHT}"
    "\N{DIGIT NINE}"
    "\N{COLON}"
    "\N{SEMICOLON}"
    "\N{LESS-THAN SIGN}"
    "\N{EQUALS SIGN}"
    "\N{GREATER-THAN SIGN}"
    "\N{QUESTION MARK}"
    "\N{COMMERCIAL AT}"
    "\N{LATIN CAPITAL LETTER A}"
    "\N{LATIN CAPITAL LETTER B}"
    "\N{LATIN CAPITAL LETTER C}"
    "\N{LATIN CAPITAL LETTER D}"
    "\N{LATIN CAPITAL LETTER E}"
    "\N{LATIN CAPITAL LETTER F}"
    "\N{LATIN CAPITAL LETTER G}"
    "\N{LATIN CAPITAL LETTER H}"
    "\N{LATIN CAPITAL LETTER I}"
    "\N{LATIN CAPITAL LETTER J}"
    "\N{LATIN CAPITAL LETTER K}"
    "\N{LATIN CAPITAL LETTER L}"
    "\N{LATIN CAPITAL LETTER M}"
    "\N{LATIN CAPITAL LETTER N}"
    "\N{LATIN CAPITAL LETTER O}"
    "\N{LATIN CAPITAL LETTER P}"
    "\N{LATIN CAPITAL LETTER Q}"
    "\N{LATIN CAPITAL LETTER R}"
    "\N{LATIN CAPITAL LETTER S}"
    "\N{LATIN CAPITAL LETTER T}"
    "\N{LATIN CAPITAL LETTER U}"
    "\N{LATIN CAPITAL LETTER V}"
    "\N{LATIN CAPITAL LETTER W}"
    "\N{LATIN CAPITAL LETTER X}"
    "\N{LATIN CAPITAL LETTER Y}"
    "\N{LATIN CAPITAL LETTER Z}"
    "\N{LEFT SQUARE BRACKET}"
    "\N{REVERSE SOLIDUS}"
    "\N{RIGHT SQUARE BRACKET}"
    "\N{LOW LINE}"
    "\N{LATIN SMALL LETTER A}"
    "\N{LATIN SMALL LETTER B}"
    "\N{LATIN SMALL LETTER C}"
    "\N{LATIN SMALL LETTER D}"
    "\N{LATIN SMALL LETTER E}"
    "\N{LATIN SMALL LETTER F}"
    "\N{LATIN SMALL LETTER G}"
    "\N{LATIN SMALL LETTER H}"
    "\N{LATIN SMALL LETTER I}"
    "\N{LATIN SMALL LETTER J}"
    "\N{LATIN SMALL LETTER K}"
    "\N{LATIN SMALL LETTER L}"
    "\N{LATIN SMALL LETTER M}"
    "\N{LATIN SMALL LETTER N}"
    "\N{LATIN SMALL LETTER O}"
    "\N{LATIN SMALL LETTER P}"
    "\N{LATIN SMALL LETTER Q}"
    "\N{LATIN SMALL LETTER R}"
    "\N{LATIN SMALL LETTER S}"
    "\N{LATIN SMALL LETTER T}"
    "\N{LATIN SMALL LETTER U}"
    "\N{LATIN SMALL LETTER V}"
    "\N{LATIN SMALL LETTER W}"
    "\N{LATIN SMALL LETTER X}"
    "\N{LATIN SMALL LETTER Y}"
    "\N{LATIN SMALL LETTER Z}"
    "\N{VERTICAL LINE}"
    "\N{TILDE}"
):
    xlate[ord(c)] = c


def fix_unicode(s):
    try:
        return str(s.translate(xlate))
    except TypeError:
        return s
