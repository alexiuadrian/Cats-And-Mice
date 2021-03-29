import numpy as np
import sys
import os
import time

# Start of timer
timer_start = time.perf_counter()

input_folder = None
output_folder = None
NSOL = None

try:
    input_folder = sys.argv[1]
except:
    print("Va rog dati fisierul de intrare")

try:
    output_folder = sys.argv[2]
except:
    print("Va rog dati fisierul de iesire")

try:
    NSOL = int(sys.argv[3])
except:
    print("Numarul de solutii nu este un intreg sau nu este deloc")
    sys.exit(0)

def import_files(folder):
    names = []

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            names.append(file)

    return names

def write_to_file(folder, filename, content):
    file = open(folder + '/' + filename, "w")
    file.write(content)

names = import_files(input_folder)

print(names)

write_to_file(output_folder, names[0], "Muie Ionescu")

# End of timer
timer_end = time.perf_counter()
print(f"Time elapsed: {timer_end - timer_start} seconds")