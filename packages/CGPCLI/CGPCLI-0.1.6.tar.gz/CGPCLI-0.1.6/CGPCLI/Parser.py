import re

from itertools import chain
from ast import literal_eval
from datetime import datetime

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
    
    date_regex = re.compile(r"(\#T(?:\d{2}-\d{2}-\d{4}_\d{2}:\d{2}:\d{2}))\s*(.*)", re.DOTALL)
    
    def parse_date(src):
        match = date_regex.match(src)
        if match is not None:
            date, src = match.groups()
            yield datetime.strptime(date, '#T%d-%m-%Y_%H:%M:%S'), src
            
    cert_regex = re.compile(r"(\[.*\])(.*)", re.DOTALL)        
    
    def parse_cert(src):
        match = cert_regex.match(src)
        if match is not None:
            sert, src = match.groups()
            yield sert, src    
                        
    string_regex = re.compile(r"(?:(?:\"([(\\\")\w\s\\\.\[\]\*/~:()#@!&<>-]*)\")|([\w\.@-]*))(.*)",
                              re.DOTALL)
    
    def parse_string(src):
        match = string_regex.match(src)
        if match is not None:
            a,b,c = match.groups()
            string = match.groups()[1] or match.groups()[0]
            src = match.groups()[2].strip()
                
            yield string, src
    
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
            parse_date(src),
            parse_cert(src),
            parse_array(src),
            parse_object(src),
            parse_true(src),
            parse_false(src),
            parse_null(src),
            parse_string(src),
            ):
            yield match
            return
    
    parse_left_bracket = parse_word("(")
    parse_right_bracket = parse_word(")")
    parse_empty_array = sequence(parse_left_bracket, parse_right_bracket)
    
    def parse_array(src):
        for _, src in parse_empty_array(src):
            yield [], src
            return
    
        for (_, items, _), src in sequence(
            parse_left_bracket,
            parse_comma_separated_values,
            parse_right_bracket,
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
    
    parse_equals = parse_word("=")
    
    def parse_keyvalue(src):
        for (key, _, value, _), src in sequence(
            parse_string,
            parse_equals,
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
    
    string = string.replace('\n', '')
    
    match = list(parse_value(string))
   
    if len(match) != 1:
        raise NotValidCGPStringError()
    
    result, src = match[0]
    
    if result is None:
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