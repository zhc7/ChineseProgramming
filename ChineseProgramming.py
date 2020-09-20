import sys
import getopt
import os


class Reader:
    def __init__(self, file):
        self.file = open(file)
        self.lines = self.file.readlines()
        self.operators = ["+", "-", "*", "/", "%"]
        self.separators = [">", "<", "=", ":", "[", "]", "(", ")", ",", "@", "!", "{", "}", ".", "的", "当", "等于"] + self.operators
        self.string_tokens = ["'", '"']
        self.output = ""
        self.keywords = {
            "如果": "if",
            "又如果": "elif",
            "否则": "else",
            "当": "while",
            "对于": "for",
            "区间": "range",
            "输入": "input",
            "打印": "print",
            "属于": "in",
            "是": "is",
            "就是": "is",
            "或": "or",
            "或者": "or",
            "且": "and",
            "并且": "and",
            "非": "not",
            "没有": "not",
            "不属于": "not in",
            "返回": "return",
            "先返回": "yield",
            "打开": "open",
            "整数": "int",
            "浮点数": "float",
            "字符串": "str",
            "定义类": "class",
            "类": "class",
            "定义": "def",
            "初始化": "__init__",
            "真": "True",
            "假": "False",
            "空": "None",
            "以": "with",
            "把": "with",
            "称作": "as",
            "退出": "break",
            "继续": "continue",
            "从": "from",
            "导入": "import",
            "跳过": "pass",
            "尝试": "try",
            "捕捉": "except",
            "最后": "finally",
            "抛出": "raise",
            "闭包": "lambda",
            "删除": "del",
            "等于": "==",
            "大于": ">",
            "小于": "<",
            "大于等于": ">=",
            "小于等于": "<=",
            "不等于": "!=",
            "的": ".",

        }
        self.keywords_list = self.keywords.keys()
        self.string_starter = None

 
    def separate(self, line):
        words = []
        length = len(line)
        word = ""

        #indent collector
        for i in range(length):
            if line[i] == " ":
                word += " "
            else:
                words.append(word)
                word = ""
                break

        #main loop
        while i < length:
            char = line[i]
            #case comment
            if char == "#":
                if word:
                    words.append(word)
                words.append(line[i:])
                return words, True

            #get change line mark
            if char == "\\":
                words.append(word)
                words.append(char)
                i += 1
                continue

            #get string
            if char in self.string_tokens:
                if word:
                    words.append(word)
                    word = ""
                string, starter, stop_index = self.collect_string(line, i)
                if not starter:
                    words.append(string)
                    i = stop_index + 1
                    continue
                else:
                    self.string_starter = starter
                    words.append(string)
                    return words, False
            
            #common situation
            if char == " ":
                #case white space
                if word:
                    words.append(word)
                    word = ""
                if words[-1] != " ":
                    words.append(" ")
            elif char in self.separators:
                #case sperator
                if word:
                    words.append(word)
                    word = ""
                last = words[-1]
                if last in self.operators and char in self.operators:
                    words.pop()
                    words.append(last + char)
                else:
                    words.append(char)
            else:
                #nothing happened
                word += char

            #move to next index
            i += 1
        if word:
            words.append(word)
        
        return words, True
    
    def collect_string(self, line, start_index, starter=None):
        i = start_index
        length = len(line)
        string = ""
        if not starter:
            if length - i > 2 and line[i:i+3] in ["'''", '"""']:
                starter = line[i:i+3]
                i = i+3
                string += starter
            else:
                starter = line[i]
                i = i+1
                string += starter
        change_meaning = False
        while i < length:
            char = line[i]

            #case 转义
            if change_meaning:
                string += "\\" + char
                change_meaning = False
                i += 1
                continue
            elif char == "\\":
                if i == len(line.rstrip()) - 1:
                    string += char
                    i += 1
                    continue
                change_meaning = True
                i += 1
                continue
            
            #字符串可能结尾时
            elif char == starter[0]:
                if char == starter:
                    string += char
                    return string, None, i
                if length - i > 2 and line[i:i+3] == starter:
                    string += line[i:i+3]
                    return string, None, i + 2
            
            #common situation
            string += char

            i += 1
        
        #未结束
        return string, starter, i


    def paraphrase(self, word):
        if word in self.keywords_list:
            #key words
            returning = self.keywords[word]
            if word in self.separators:
                returning += " "
            return returning
        return word

    def parse(self):
        length = len(self.lines)
        i = 0
        flag = None
        words = []
        while i < length:
            line = self.lines[i]
            
            #case not end
            if flag:
                if flag == "string":
                    string, starter, end = self.collect_string(line, 0, self.string_starter)
                    words.append(string)
                    if not starter:
                        self.string_starter = None
                        line = line[end + 1:]
                        flag = None
                    else:
                        i += 1
                        continue
                elif flag == "common":
                    pass
            
            #common situation
            res_words, isend = self.separate(line)
            words += res_words

            if not isend:
                if words[-1][0] in ['"', "'"]:
                    flag = "string"
                else:
                    flag = "common"

            #paraphrase the words
            for word in words:
                w = self.paraphrase(word)
                self.output += w
            words = []
            i += 1
    
    def write_output(self, filename):
        with open(filename, "w") as f:
            f.write(self.output)



if __name__ == "__main__":
    args = sys.argv[-2:]
    input_file, output_file = args
    reader = Reader(input_file)
    reader.parse()
    if output_file == "/":
        output_file = input_file.strip(".cpy") + ".py"
    if len(output_file) < 4 or output_file[-3:] != ".py":
        output_file += ".py"
    if not os.path.exists(".CP_TEMP"):
        os.makedirs(".CP_TEMP")
    reader.write_output(".CP_TEMP/" + output_file)


