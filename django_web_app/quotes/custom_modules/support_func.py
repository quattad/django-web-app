import html

def parse_content(input_string):
    return html.unescape(input_string.replace("<p>", "").replace("</p>", "").replace("<br />", ""))