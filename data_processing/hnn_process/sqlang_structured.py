import re

import inflection
import sqlparse
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# Define token types as constants
OTHER = 0
FUNCTION = 1
BLANK = 2
KEYWORD = 3
INTERNAL = 4
TABLE = 5
COLUMN = 6
INTEGER = 7
FLOAT = 8
HEX = 9
STRING = 10
WILDCARD = 11
SUBQUERY = 12
DUD = 13

# Define a dictionary to map token types to their string representations
ttypes = {
    0: "OTHER", 1: "FUNCTION", 2: "BLANK", 3: "KEYWORD", 4: "INTERNAL",
    5: "TABLE", 6: "COLUMN", 7: "INTEGER", 8: "FLOAT", 9: "HEX",
    10: "STRING", 11: "WILDCARD", 12: "SUBQUERY", 13: "DUD",
}

# Regular expression patterns for tokenizing SQL code
scanner = re.Scanner([
    (r"\[[^\]]*\]", lambda scanner, token: token),
    (r"\+", lambda scanner, token: "REGPLU"),
    (r"\*", lambda scanner, token: "REGAST"),
    (r"%", lambda scanner, token: "REGCOL"),
    (r"\^", lambda scanner, token: "REGSTA"),
    (r"\$", lambda scanner, token: "REGEND"),
    (r"\?", lambda scanner, token: "REGQUE"),
    (r"[\.~``;_a-zA-Z0-9\s=:\{\}\-\\]+", lambda scanner, token: "REFRE"),
    (r'.', lambda scanner, token: None),
])


# Tokenizer function for regular expressions
def tokenizeRegex(s):
    results = scanner.scan(s)[0]
    return results


class SqlangParser:
    def __init__(self, sql, regex=False, rename=True):
        self.sql = self.sanitizeSql(sql)
        self.idMap = {"COLUMN": {}, "TABLE": {}}
        self.idMapInv = {}
        self.idCount = {"COLUMN": 0, "TABLE": 0}
        self.regex = regex
        self.parseTreeSentinel = False
        self.tableStack = []
        self.parse = sqlparse.parse(self.sql)
        self.parse = [self.parse[0]]
        self.removeWhitespaces(self.parse[0])
        self.identifyLiterals(self.parse[0])
        self.parse[0].ptype = SUBQUERY
        self.identifySubQueries(self.parse[0])
        self.identifyFunctions(self.parse[0])
        self.identifyTables(self.parse[0])
        self.parseStrings(self.parse[0])
        if rename:
            self.renameIdentifiers(self.parse[0])
        self.tokens = self.getTokens(self.parse)

    @staticmethod
    def sanitizeSql(sql):
        s = sql.strip().lower()
        if not s[-1] == ";":
            s += ';'
        s = re.sub(r'\(', r' ( ', s)
        s = re.sub(r'\)', r' ) ', s)
        words = ['index', 'table', 'day', 'year', 'user', 'text']
        for word in words:
            s = re.sub(r'([^\w])' + word + '$', r'\1' + word + '1', s)
            s = re.sub(r'([^\w])' + word + '(\W)', r'\1' + word + '1\2', s)
        return s

    def removeWhitespaces(self, p):
        if hasattr(p, 'tokens'):
            p.tokens = [token for token in p.tokens if not token.is_whitespace]
            for token in p.tokens:
                self.removeWhitespaces(token)

    def identifyLiterals(self, p):
        if hasattr(p, 'tokens'):
            for token in p.tokens:
                if token.ttype in sqlparse.tokens.Literal.String:
                    token.ttype = STRING
                    token.parent = p
                elif token.ttype is sqlparse.tokens.Name.Placeholder:
                    token.ttype = STRING
                    token.parent = p
                elif token.ttype in sqlparse.tokens.Literal.Number.Integer:
                    token.ttype = INTEGER
                    token.parent = p
                elif token.ttype in sqlparse.tokens.Literal.Number.Float:
                    token.ttype = FLOAT
                    token.parent = p
                elif token.ttype in sqlparse.tokens.Comment:
                    token.ttype = INTERNAL
                    token.parent = p
                else:
                    token.ttype = OTHER
                    token.parent = p
                self.identifyLiterals(token)

    def identifySubQueries(self, p):
        if hasattr(p, 'tokens'):
            for token in p.tokens:
                if token.ttype == sqlparse.tokens.DML and token.value.upper() != 'SELECT':
                    token.ttype = INTERNAL
                self.identifySubQueries(token)

    def identifyFunctions(self, p):
        if hasattr(p, 'tokens'):
            for token in p.tokens:
                if token.ttype == sqlparse.tokens.Keyword and token.value.upper() == 'SELECT':
                    if p.tokens.index(token) + 1 < len(p.tokens):
                        if p.tokens[p.tokens.index(token) + 1].ttype == sqlparse.tokens.Operator:
                            continue
                elif token.ttype == sqlparse.tokens.Name.Function:
                    token.ttype = FUNCTION
                self.identifyFunctions(token)

    def identifyTables(self, p):
        if hasattr(p, 'tokens'):
            for token in p.tokens:
                if token.ttype == sqlparse.tokens.Keyword and token.value.upper() == 'FROM':
                    self.tableStack.append(token.parent)
                if token.ttype == sqlparse.tokens.Name and token.parent.ttype != sqlparse.tokens.Function:
                    token.ttype = TABLE
                    token.parent = p
                    if not token.value in self.idMap["TABLE"]:
                        self.idMap["TABLE"][token.value] = "TBL_" + str(self.idCount["TABLE"])
                        self.idMapInv["TBL_" + str(self.idCount["TABLE"])] = token.value
                        self.idCount["TABLE"] += 1
                    self.tableStack[-1].parent = token
                self.identifyTables(token)
            if p.tokens:
                lastToken = p.tokens[-1]
                if lastToken.ttype == sqlparse.tokens.Punctuation and lastToken.value == ';':
                    if len(self.tableStack) > 0:
                        self.tableStack.pop()

    def parseStrings(self, p):
        if hasattr(p, 'tokens'):
            for token in p.tokens:
                if token.ttype == STRING and not token.value.startswith("'") and not token.value.startswith('"'):
                    token.ttype = COLUMN
                    token.parent = p
                    if not token.value in self.idMap["COLUMN"]:
                        self.idMap["COLUMN"][token.value] = "COL_" + str(self.idCount["COLUMN"])
                        self.idCount["COLUMN"] += 1
                self.parseStrings(token)

    def renameIdentifiers(self, p):
        if hasattr(p, 'tokens'):
            for token in p.tokens:
                if token.ttype == FUNCTION or token.ttype == TABLE or token.ttype == COLUMN:
                    if hasattr(token, 'parent') and token.parent:
                        if token.parent.ttype == FUNCTION or token.parent.ttype == TABLE or token.parent.ttype == COLUMN:
                            continue
                    if token.ttype == FUNCTION:
                        token.value = inflection.underscore(token.value).replace('_', ' ')
                    elif token.ttype == TABLE or token.ttype == COLUMN:
                        token.value = inflection.singularize(token.value.replace('_', ' '))
                    if token.value in self.idMapInv:
                        token.value = self.idMapInv[token.value]
                self.renameIdentifiers(token)

    def getTokens(self, parseTree):
        tokens = []
        for item in parseTree:
            if hasattr(item, 'tokens'):
                tokens += self.getTokens(item.tokens)
            else:
                tokens.append(item)
        return tokens

    def lemmatize(self, word):
        lemmatizer = WordNetLemmatizer()
        pos = self.getWordNetPos(pos_tag([word])[0][1])
        if pos:
            return lemmatizer.lemmatize(word, pos)
        else:
            return lemmatizer.lemmatize(word)

    @staticmethod
    def getWordNetPos(tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def generateTokens(self):
        tokens = []
        for token in self.tokens:
            tokenType = token.ttype
            if tokenType == FUNCTION:
                tokens.append("FUNCTION")
            elif tokenType == BLANK:
                tokens.append("BLANK")
            elif tokenType == KEYWORD:
                tokens.append("KEYWORD")
            elif tokenType == INTERNAL:
                tokens.append("INTERNAL")
            elif tokenType == TABLE:
                tokens.append("TABLE")
            elif tokenType == COLUMN:
                tokens.append("COLUMN")
            elif tokenType == INTEGER:
                tokens.append("INTEGER")
            elif tokenType == FLOAT:
                tokens.append("FLOAT")
            elif tokenType == HEX:
                tokens.append("HEX")
            elif tokenType == STRING:
                tokens.append("STRING")
            elif tokenType == WILDCARD:
                tokens.append("WILDCARD")
            elif tokenType == SUBQUERY:
                tokens.append("SUBQUERY")
            elif tokenType == DUD:
                tokens.append("DUD")
            else:
                tokens.append("OTHER")
        return tokens

    def tokenize(self):
        if self.regex:
            return tokenizeRegex(self.sql)
        else:
            return self.generateTokens()

    def get_token_types(self):
        return [ttypes[token.ttype] for token in self.tokens]

    def get_identifiers(self):
        identifiers = []
        for token in self.tokens:
            if token.ttype == TABLE or token.ttype == COLUMN:
                identifiers.append(token.value)
        return identifiers


# Usage example
sql = """
SELECT *
FROM users
WHERE users.id = 10
"""
parser = SqlangParser(sql)
token_types = parser.get_token_types()
identifiers = parser.get_identifiers()

print("Token Types:")
print(token_types)
print("Identifiers:")
print(identifiers)
