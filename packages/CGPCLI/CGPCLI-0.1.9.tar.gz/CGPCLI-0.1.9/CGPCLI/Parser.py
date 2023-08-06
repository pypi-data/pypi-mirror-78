from datetime import datetime

from CGPCLI.Errors import NotValidCGPStringError

def parse_to_CGP_object(python_object):
    result = ''
    
    if isinstance(python_object,int):
        result += '"#' + str(python_object) + '"'
    
    elif isinstance(python_object,str):
        result += '"' + python_object + '"'
    
    elif isinstance(python_object,datetime):
        result += datetime.strftime(python_object, '#T%d-%m-%Y_%H:%M:%S')
        
    elif isinstance(python_object,dict):
        result += '{' + ''.join(f'"{str(x)}" = {parse_to_CGP_object(y)};' for x, y in zip(list(python_object.keys()), list(python_object.values()))) + '}'
            
    elif isinstance(python_object,list):
        result += '(' + ''.join(parse_to_CGP_object(x) + ', ' for x in python_object)[:-2] + ')'
        
    return result

def parse_to_python_object(string, from_CLI=True):
    def preparse_from_CLI(string):
        string = string.replace('\n', '')  
    
    def parse_array(string):
        result_arr = list()
        values = string[1:-1]
        
        pos = values.find(',')
        el = values
        
        while pos != -1:            
            el = values[:pos]
            while el.count('"')%2 != 0:
                pos = values.find(',', pos+1)
                el = values[:values.find(',', pos+1)]
    
            while el.count('(') != el.count(')'):
                pos = values.find(')', pos+1)
                el = values[:pos + 1]
                
            result_arr.append(parse_to_python_object(el.strip()))
            
            values = values[pos+1:]
            if values.startswith(','):
                values = values[1:]
            pos = values.find(',')

        values = values.strip()
        
        if values != '':
            result_arr.append(parse_to_python_object(values))

        return result_arr
    
    def parse_dict(string):
        result_dict = dict()
        values = string[1:-1]
        
        pos = values.find(';')
        el = values
        
        while pos != -1:
            el = values[:pos]
            while el.count('"')%2 != 0:
                el = values[:values.find(',', pos+1)]
                pos = values.find(',', pos+1)
                
            while el.count('{') != el.count('}'):
                pos = values.find('};', pos+1) + 1
                el = values[:pos]            
                
            k = el[:el.find('=')]
            v = el[el.find('=')+1:]
    
            result_dict.update({k.strip().replace('"',''): parse_to_python_object(v.strip())})
            
            values = values[pos+1:]
            pos = values.find(';')
    
        return result_dict
        
    string.strip()
    
    if from_CLI:
        preparse_from_CLI(string)
        
    #if dict
    if string[0] == '{':
        return parse_dict(string)
    #if arr
    elif string[0] == '(':
        return parse_array(string)
    else:
        if string[0] == '"' and string[-1] == '"':
            string = string[1:-1]
            
        if string.startswith('#T'):
            string = datetime.strptime(string, '#T%d-%m-%Y_%H:%M:%S')
            
        if string == 'true':
            string = True
        
        if string == 'false':
            string = False
            
        return string