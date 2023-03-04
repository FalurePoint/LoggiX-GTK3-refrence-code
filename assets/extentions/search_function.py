def get_line(file, working_line):
    with open(file, 'r') as file:
        lines = file.readlines()
        line = lines[working_line - 1]
        return line


def line_has(file, line, search_term):
    line_number = line
    with open(file) as f:
        for i, line in enumerate(f):
            if i == line_number:
                working_line = line.strip()
                if search_term in working_line:
                    #content = get_line(file, working_line)
                    return True
                else:
                    return False
