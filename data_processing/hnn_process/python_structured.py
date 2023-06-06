import re
import token
import tokenize
from io import StringIO

import inflection
from nltk import pos_tag
from nltk import wordpunct_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


class PythonParser:
    def __init__(self, code):
        self.code = code
        self.varnames = set()
        self.tokenized_code = []
        self.bool_failed_var = False
        self.bool_failed_token = False
        self.wnler = WordNetLemmatizer()
        self.pattern_var_equal = re.compile(r"(\s*[_a-zA-Z][_a-zA-Z0-9]*\s*)(,\s*[_a-zA-Z][_a-zA-Z0-9]*\s*)*=")
        self.pattern_var_for = re.compile(r"for\s+[_a-zA-Z][_a-zA-Z0-9]*\s*(,\s*[_a-zA-Z][_a-zA-Z0-9]*)*\s+in")
        self.pattern_case1_in = re.compile(r"In ?\[\d+\]: ?")
        self.pattern_case1_out = re.compile(r"Out ?\[\d+\]: ?")
        self.pattern_case1_cont = re.compile(r"( )+\.+: ?")
        self.pattern_case2_in = re.compile(r">>> ?")
        self.pattern_case2_cont = re.compile(r"\.\.\. ?")
        self.patterns = [
            self.pattern_case1_in,
            self.pattern_case1_out,
            self.pattern_case1_cont,
            self.pattern_case2_in,
            self.pattern_case2_cont
        ]

    def repair_program_io(self, code):
        lines = code.split("\n")
        lines_flags = [0 for _ in range(len(lines))]
        code_list = []

        for line_idx in range(len(lines)):
            line = lines[line_idx]
            for pattern_idx in range(len(self.patterns)):
                if re.match(self.patterns[pattern_idx], line):
                    lines_flags[line_idx] = pattern_idx + 1
                    break
        lines_flags_string = "".join(map(str, lines_flags))
        bool_repaired = False

        if lines_flags.count(0) == len(lines_flags):
            repaired_code = code
            code_list = [code]
            bool_repaired = True

        elif re.match(re.compile(r"(0*1+3*2*0*)+"), lines_flags_string) or \
                re.match(re.compile(r"(0*4+5*0*)+"), lines_flags_string):
            repaired_code = ""
            pre_idx = 0
            sub_block = ""
            if lines_flags[0] == 0:
                flag = 0
                while (flag == 0):
                    repaired_code += lines[pre_idx] + "\n"
                    pre_idx += 1
                    flag = lines_flags[pre_idx]
                sub_block = repaired_code
                code_list.append(sub_block.strip())
                sub_block = ""

            for idx in range(pre_idx, len(lines_flags)):
                if lines_flags[idx] != 0:
                    repaired_code += re.sub(self.patterns[lines_flags[idx] - 1], "", lines[idx]) + "\n"

                    if len(sub_block.strip()) and (idx > 0 and lines_flags[idx - 1] == 0):
                        code_list.append(sub_block.strip())
                        sub_block = ""
                    sub_block += re.sub(self.patterns[lines_flags[idx] - 1], "", lines[idx]) + "\n"

                else:
                    if len(sub_block.strip()) and (idx > 0 and lines_flags[idx - 1] != 0):
                        code_list.append(sub_block.strip())
                        sub_block = ""
                    sub_block += lines[idx] + "\n"

            if len(sub_block.strip()):
                code_list.append(sub_block.strip())

            bool_repaired = True

        else:
            code_list.append(code)

        return bool_repaired, repaired_code, code_list

    def repair_program_token(self, code_list):
        repaired_code_list = []
        for code in code_list:
            self.tokenized_code = []
            try:
                self.tokenize_python_code(code)
                repaired_code = self.get_repaired_code(code)
                repaired_code_list.append(repaired_code)
            except Exception:
                self.bool_failed_token = True
                repaired_code_list.append(code)

        return repaired_code_list

    def tokenize_python_code(self, code):
        tokens = tokenize.generate_tokens(StringIO(code).readline)
        for token_type, _, start, _, _ in tokens:
            if token_type == token.NAME:
                self.varnames.add(code[start[0]:start[1]])

            self.tokenized_code.append(token.tok_name[token_type])

    def get_repaired_code(self, code):
        for name in self.varnames:
            if name in code:
                if re.match(self.pattern_var_equal, code):
                    code = self.repair_variable_assignment(code, name)

                if re.match(self.pattern_var_for, code):
                    code = self.repair_variable_iteration(code, name)

                if re.match(r"(\s*" + re.escape(name) + "\s*[,)\n])", code):
                    code = self.repair_variable_usage(code, name)

        return code

    def repair_variable_assignment(self, code, name):
        # Find all occurrences of the variable assignment
        matches = re.findall(r"(\b" + re.escape(name) + r"\b\s*=)", code)
        for match in matches:
            code = code.replace(match, "self." + match)
        return code

    def repair_variable_iteration(self, code, name):
        # Find all occurrences of the variable in for loops
        matches = re.findall(r"(for\s+" + re.escape(name) + r"\b\s*(?:,\s*[_a-zA-Z][_a-zA-Z0-9]*)*\s+in)", code)
        for match in matches:
            code = code.replace(match, match.replace(name, "self." + name))
        return code

    def repair_variable_usage(self, code, name):
        # Find all occurrences of the variable usage
        matches = re.findall(r"(\b" + re.escape(name) + r"\b\s*[,)\n])", code)
        for match in matches:
            code = code.replace(match, "self." + match)
        return code

    def repair_program(self):
        # Repair program based on IO and token errors
        bool_repaired_io, repaired_code_io, code_list_io = self.repair_program_io(self.code)
        repaired_code_token = self.repair_program_token(code_list_io)

        # Combine the repaired code from IO and token repairs
        if self.bool_failed_var:
            final_code = self.code
        else:
            final_code = repaired_code_token[-1] if self.bool_failed_token else repaired_code_token[-1] if \
            repaired_code_token[-1] else self.code

        return final_code


class PythonRefactor:
    def __init__(self, code):
        self.parser = PythonParser(code)

    def add_comments(self, code):
        # Add comments to the code
        lines = code.split("\n")
        for line_idx in range(len(lines)):
            line = lines[line_idx]
            if line.strip().startswith("#"):
                continue

            line_tokens = wordpunct_tokenize(line)
            line_tags = pos_tag(line_tokens)

            for i in range(len(line_tags)):
                token, tag = line_tags[i]
                if tag.startswith("N") or tag.startswith("V"):
                    lemma = self.parser.wnler.lemmatize(token, wordnet.VERB) if tag.startswith(
                        "V") else self.parser.wnler.lemmatize(token)
                    plural = inflection.pluralize(lemma)

                    if plural != lemma and plural in self.parser.varnames:
                        lines[line_idx] = lines[line_idx][:line.find(token)] + token + "  # variable name: " + plural + \
                                          lines[line_idx][line.find(token) + len(token):]
                        break

        code_with_comments = "\n".join(lines)
        return code_with_comments

    def refactor(self):
        # Repair the program
        repaired_code = self.parser.repair_program()

        # Add comments to the repaired code
        code_with_comments = self.add_comments(repaired_code)

        return code_with_comments


# Example usage:
code = """
x = 10
y = 20

for i in range(x):
    print(i)

if x > y:
    print("x is greater than y")
else:
    print("x is less than or equal to y")
"""

refactorer = PythonRefactor(code)
refactored_code = refactorer.refactor()
print(refactored_code)
