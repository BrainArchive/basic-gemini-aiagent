import sys
import os.path
if len(sys.argv) < 2:
    print("PROVIDE A PROMPT!")
    sys.exit(1)
bread = sys.argv[1:]

print(bread)
print(os.path.abspath("."))

