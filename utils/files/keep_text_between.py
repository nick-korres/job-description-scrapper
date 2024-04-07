

def keep_text_between(file_path, start_string, end_string ):
    with open(file_path, 'r',encoding='utf-8') as input_file:
        # Read the entire contents of the input file
        file_contents = input_file.read()

        # Find the indices of the start and end strings
        start_index = file_contents.find(start_string) + len(start_string)
        end_index = file_contents.find(end_string)

        # Extract the substring between the start and end strings
        substring = file_contents[start_index:end_index]


        if substring =="" or substring == None:
           raise Exception("ERROR: No text found between the start and end strings")
        
        return substring 