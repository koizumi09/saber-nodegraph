    
import json

Start = "Start"

def parse_text_elements(content):
    START_TAG = "## Text Elements"
    END_TAG = "%%"

    start_index = content.find(START_TAG)
    end_index = content.find(END_TAG)

    content = content[start_index + len(START_TAG):end_index]

    ID_START = " ^"

    content = content.split("\n")

    line_count = 1
    text_dict = {}
    for line in content:
        if line.strip():
            line, index = line.split(ID_START, 1)
            text_dict[index] = line
            line_count += 1

    return text_dict

def parse_drawing(content):
    START_TAG = "## Drawing"
    END_TAG = "%%"

    start_index = content.find(START_TAG)
    end_index = content.find(END_TAG, start_index)

    content = content[start_index + len(START_TAG):end_index]

    JSON_START = "```json"
    JSON_END = "```"

    start_index = content.find(JSON_START)
    end_index = content.rfind(JSON_END)

    content = content[start_index:end_index]
    content = content.replace(JSON_START, "", 1)
    
    return json.loads(content.strip())

def parse_json(content):
    return json.loads(content)
    