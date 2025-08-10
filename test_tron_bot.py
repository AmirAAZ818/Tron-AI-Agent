import subprocess

multi_turn_input = """\
2 0
9 5 9 5
10 7 10 7
2 0
10 5 10 5
11 7 11 7
2 0
15 10 15 10
14 9 14 9
2 0
0 0 0 0
1 1 1 1
2 0
28 19 28 19
29 18 29 18
"""

process = subprocess.Popen(
    ['python', 'tron_bot.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)
output, _ = process.communicate(multi_turn_input)
print("Full Agent Output:\n", output)
