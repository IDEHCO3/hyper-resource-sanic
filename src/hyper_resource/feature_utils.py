import json

def set_html_variables(html_content: str, title:str, jsonld: str) -> str:
    TITLE_VARIABLE = "{{title}}"
    JSONLD_VARIABLE = "{{jsonld}}"
    content = html_content.replace(TITLE_VARIABLE, title)

    content = content.replace( JSONLD_VARIABLE, jsonld )
    return content