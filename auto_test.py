import pyautogui as key
import time
file_object = open('test_sequence.txt', 'r')
print("Starting Macro in 5 seconds")
time.sleep(5)
commands = file_object.readline()
commands = commands.split(',')
for command in range(len(commands)):
    print("{} Was Written to the console".format(commands[command]))
    key.write(commands[command])
    key.press('enter')
    time.sleep(2)
print("This Concludes the Automatic Tests")
