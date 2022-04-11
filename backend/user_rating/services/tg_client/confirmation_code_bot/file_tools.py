def read_from_file(filename: str):
    with open(filename, 'r') as file:
        return file.read()


def write_to_file(text: str, filename: str):
    with open(filename, 'w') as file:
        return file.write(text)