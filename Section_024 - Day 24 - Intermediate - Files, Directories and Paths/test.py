# file = open("test.txt", "r")
# content = file.read()
# print(content)
# file.close()

with open("test.txt", "w") as file:
    file.write(f"Starting\n\n")

for i in range(10):
    with open("test.txt", "a") as file:
        file.write(f"Line {i+1}\n")

with open("test.txt", "r") as file:
    content = file.read()
    print(content)
