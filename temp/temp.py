# Sample input: "[1, 2, 3]" or "['a', 'b', 'c']"
input_string = input()  # e.g., "[1, 2, 3]"

# Strip the brackets and split the string by commas
input_string = input_string.strip("[]")  # Removes leading and trailing brackets
elements = input_string.split(",")  # Splits by comma

# Remove leading/trailing spaces and convert each element to the appropriate type
elements = [element.strip() for element in elements]

# Now, you'll need to check the type of each element (whether it's an int, float, or string)
converted_elements = []
for i in elements:
   converted_elements.append(int(i))
print(max(converted_elements))
