"""!d6 <number of dice> returns a string of d6 for shadowrun"""
import random
import re

def dice(n):
    hits = 0
    string = []
    glitch_status = []
    for i in range(n):
        value = random.randint(1,6)
        string.append(value)
        if value > 4:
            hits += 1
        if string.count(1)/float(n) > .5:
            if hits == 0:
                glitch_status = "critical"
            else:
                glitch_status = "glitch"
        else:
            glitch_status = "none"
    return hits, string, glitch_status
	
def parse_results(n):
    string = ''
    tuple = dice(n)
    if tuple[2] == 'none':
        string = 'You rolled `%s` and got *%s hit(s)*' % (tuple[1], tuple[0])
    if tuple[2] == 'glitch':
        string = 'You rolled `%s` and got *%s hit(s)* but unfortunately `GLITCHED`' % (tuple[1], tuple[0])
    if tuple[2] == 'critical':
        string = 'You rolled `%s` and `CRITICALLY GLITCHED`' % tuple[1]
    return string

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!d6 (\d+)", text)
    if not match:
        return

    return parse_results(int(match[0]))