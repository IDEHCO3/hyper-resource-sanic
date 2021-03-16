import re
def convert_camel_case_to_hifen(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def convert_camel_case_to_underline(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convert_underline_to_camel_case(underline_string:str) -> str:
    snippets = underline_string.split("_")
    capitalized_snippets = [s.capitalize() for s in snippets]
    return "".join(capitalized_snippets)
