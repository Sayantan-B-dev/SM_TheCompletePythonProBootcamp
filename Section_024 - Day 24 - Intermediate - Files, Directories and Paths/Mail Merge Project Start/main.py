#Create a letter using starting_letter.txt
with open("Input/Letters/starting_letter.txt", mode="r") as file:
    letter = file.read()


#for each name in invited_names.txt
with open("Input/Names/invited_names.txt", mode="r") as file:
    names = file.readlines()


#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
for name in names:
    cleaned_name=name.strip()
    new_letter = letter.replace("[name]", cleaned_name)

    with open(f"Output/ReadyToSend/letter_for_{cleaned_name}.txt", mode="w") as file:
        file.write(new_letter)
