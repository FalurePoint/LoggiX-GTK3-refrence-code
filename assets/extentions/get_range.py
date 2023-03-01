def get_from_file(filename, start_line, end_line):
    lines = []
    with open(filename, 'r') as f:
        for line_number, line in enumerate(f, 1):
            if line_number == start_line:
                lines.append(line.strip())
            elif line_number > start_line and line_number <= end_line:
                lines.append(line.strip())
            elif line_number > end_line:
                break
    if not lines:
        with open(filename, 'r') as f:
            for line_number, line in enumerate(f, 1):
                if line_number == end_line:
                    lines.append(line.strip())
                    break
    final = '\n'.join(lines)
    return final


def get_from_string(input, start_line, end_line):
    lines = input.split("\n")
    if start_line > len(lines) or start_line < 1:
        return ""
    if end_line > len(lines):
        end_line = len(lines)
    return "\n".join(lines[start_line-1:end_line])
