from itertools import chain
from ast import literal_eval
import re

from CGPCLI.Errors import NotValidCGPStringError

def parse_to_python_object(string):
    def sequence(*funcs):
        if len(funcs) == 0:
            def result(src):
                yield (), src
            return result
        def result(src):
            for arg1, src in funcs[0](src):
                for others, src in sequence(*funcs[1:])(src):
                    yield (arg1,) + others, src
        return result
    
    number_regex = re.compile(r"(\#(?:0|[1-9]\d*)(?:\.\d+)?)\s*(.*)", re.DOTALL) #(r"(\#(?:-?0?\S*)(?:\.\d+)?)\s*(.*)
    
    def parse_number(src):
        match = number_regex.match(src)
        if match is not None:
            number, src = match.groups()
            yield int(number[1:]), src
    
    date_regex = re.compile(r"(\#T(?:\d{2}-\d{2}-\d{4}_\d{2}:\d{2}:\d{2}))\s*(.*)", re.DOTALL)
    
    def parse_date(src):
        match = date_regex.match(src)
        if match is not None:
            date, src = match.groups()
            yield date[2:12] + ' ' + date[13:], src
                    
    ip_regex = re.compile(r"(\#I(?:\S*)(?:\.\d+)?)\s*(.*)", re.DOTALL)
        
    def parse_ip(src):
        match = ip_regex.match(src)
        if match is not None:
            ip, src = match.groups()
            yield literal_eval(ip[1:]), src
                        
    string_regex = re.compile(r"(\"(?:(?:\"[\w\s]*\")?(?:[^\"]*))\")\s*(.*)", re.DOTALL)
    #(\"(?:[^\\']|\\['\\bfnrt]|\\u[0-9a-fA-F]{4})*?)\"\s*(.*) not full
    def parse_string(src):
        match = string_regex.match(src)
        if match is not None:
            string, src = match.groups()
            if string.count('"') == 4:
                string = f'\'{string[1:-1]}\''
            yield literal_eval(string), src
    
    def parse_word(word, value=None):
        l = len(word)
        def result(src):
            if src.startswith(word):
                yield value, src[l:].lstrip()
        result.__name__ = "parse_%s" % word
        return result
    
    parse_true = parse_word("true", True)
    parse_false = parse_word("false", False)
    parse_null = parse_word("null", None)
    
    def parse_value(src):
        for match in chain(
            parse_string(src),
            parse_ip(src),
            parse_number(src),
            parse_date(src),
            parse_array(src),
            parse_object(src),
            parse_true(src),
            parse_false(src),
            parse_null(src),
            ):
            yield match
            return
    
    parse_left_square_bracket = parse_word("(")
    parse_right_square_bracket = parse_word(")")
    parse_empty_array = sequence(parse_left_square_bracket, parse_right_square_bracket)
    
    def parse_array(src):
        for _, src in parse_empty_array(src):
            yield [], src
            return
    
        for (_, items, _), src in sequence(
            parse_left_square_bracket,
            parse_comma_separated_values,
            parse_right_square_bracket,
            )(src):
            yield items, src
    
    parse_comma = parse_word(",")
    
    def parse_comma_separated_values(src):
        for (value, _, values), src in sequence(
            parse_value,
            parse_comma,
            parse_comma_separated_values
            )(src):
            yield [value] + values, src
            return
    
        for value, src in parse_value(src):
            yield [value], src
    
    parse_left_curly_bracket = parse_word("{")
    parse_right_curly_bracket = parse_word("}")
    parse_semicolomn = parse_word(";")
    parse_empty_object = sequence(parse_left_curly_bracket, parse_right_curly_bracket)
    
    def parse_object(src):
        for _, src in parse_empty_object(src):
            yield {}, src
            return
        for (_, items, _), src in sequence(
            parse_left_curly_bracket,
            parse_semicolomn_separated_keyvalues,
            parse_right_curly_bracket,
            )(src):
            yield items, src
    
    parse_colon = parse_word("=")
    
    def parse_keyvalue(src):
        for (key, _, value, _), src in sequence(
            parse_string,
            parse_colon,
            parse_value,
            parse_semicolomn,
            )(src):
            yield {key: value}, src
    
    def parse_semicolomn_separated_keyvalues(src):
        for (keyvalue, keyvalues), src in sequence(
            parse_keyvalue,
            parse_semicolomn_separated_keyvalues,
            )(src):
            keyvalue.update(keyvalues)
            yield keyvalue, src
            return
    
        for keyvalue, src in parse_keyvalue(src):
            yield keyvalue, src
    
    def preparse(s):
        s = s.split('\n')
        string_regex = re.compile(r"([\w*0-9-\/\.!\[\]\#:@]+)([^-\w\"#]*)(.*)", re.DOTALL)
    
        for i in range(len(s)):
            s[i] = s[i].strip().replace('\e', '\\n')
            
            #try to find "x = ..." seq
            match = string_regex.match(s[i])
            if match is not None:
                
                s[i] = '"' + match.groups()[0] + '"' + match.groups()[1]
    
                match_next = string_regex.match(match.groups()[2])

                if match_next is not None:
    
                    if match_next.groups()[2] == '':
                        #numbers
                        #check numbers
                        s[i] += '"' + match_next.groups()[0] + '"' + match_next.groups()[1]
                       
                        continue
                    
                    s[i] += ''.join(preparse(''.join(match_next.groups())))
                
                #"" && "-1"
                else:
                    s[i] += match.groups()[2]
               
    
            else:
                #try to find "..." values
                half_string_regex = re.compile(r'\"([\w*0-9-\/ \.!|\#\[\];]+)\"(.*)', re.DOTALL)
                
                match = half_string_regex.match(s[i])
                if match is not None:
                    s[i] = '"' + match.groups()[0] + '"'
                    
                    string_parts_regex = re.compile(r'([^-\w\"]*)([\w*0-9-\/\.!|\#]+)([^-\w\"]*)(.*)', re.DOTALL)
                    match_next = string_parts_regex.match(match.groups()[1])
                    
                    if match_next is not None:
                        
                        s[i] += match_next.groups()[0] + '"' + match_next.groups()[1] + '"' + match_next.groups()[2]
                    
                        s[i] += ''.join(preparse(match_next.groups()[3]))
                    
                    else:
                        s[i] += match.groups()[1]
                     
                #try to parse objects   
                else:
                    last_chance = re.compile(r'(.)\"?([\w*0-9-\/ \.!|\#\[\];]+)\"?([^\w])(.*)', re.DOTALL)
                    match = last_chance.match(s[i])
                    
                    if match is not None:                        
                        s[i] = match.groups()[0] + '"' + match.groups()[1] + '"' + match.groups()[2]
                    
                        s[i] += ''.join(preparse(match.groups()[3]))
                         
        return ''.join(s)
    
    string = preparse(string)
    
    match = list(parse_value(string))
   
    if len(match) != 1:
        raise NotValidCGPStringError()
    
    result, src = match[0]
    
    if src.strip():
        raise NotValidCGPStringError()
    return result    

def parse_to_CGP_object(python_object):
    result = ''
    
    if isinstance(python_object,int):
        result += '"#' + str(python_object) + '"'
    elif isinstance(python_object,str):
        result += '"' + python_object + '"'
        
    elif isinstance(python_object,dict):
        result += '{' + ''.join(f'"{str(x)}" = {parse_to_CGP_object(y)};' for x, y in zip(list(python_object.keys()), list(python_object.values()))) + '}'
            
    elif isinstance(python_object,list):
        result += '(' + ''.join(parse_to_CGP_object(x) + ', ' for x in python_object)[:-2] + ')'
        
    return result