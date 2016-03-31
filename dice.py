"""!dice <dice string> returns a string of dice totals"""
import re
from random import randint

def dice_roller(amount, sides):
    values = []
    if amount > 0:
        for i in range(amount):
            values.append(randint(1, sides))
        total = sum(values)
        return values, total
    else:
        return 0

def parse_dice(dice_input):
    parsed_dice = dice_input.partition('d')
    
    if parsed_dice[0] == '':
        amount = 1
    else:
        amount = int(parsed_dice[0])
    
    sides = int(parsed_dice[2])
    
    return dice_roller(amount, sides)

def replace_dice(input_string):
    pattern = re.compile(r'([^\s]*d[^\s]+)')
    parsed_dice = []
    raw_values = []
    total_values = []
    
    for i in re.findall(pattern, input_string):
        parsed_dice.append(parse_dice(i))

    for i in parsed_dice:
        raw_values.append(str(i[0]))
        total_values.append(str(i[1]))
        
    def replace_with(data):
        def replacer(match):
            return next(data)
        return replacer

    return_string = re.sub(pattern, replace_with(iter(raw_values)), input_string)
    return_total = eval(re.sub(pattern, replace_with(iter(total_values)), input_string))
    
    return return_string, return_total

def slack_print(input_string):
    new_string = replace_dice(input_string)
    string = new_string[0]
    total = new_string[1]
    
    string = "You rolled: `" + str(string) + "` for a total of: *" + str(total) + "*"
	
    return string

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!dice (.*)", text)
    if not match:
        return

    return slack_print(str(match[0]))
