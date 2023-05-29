#from assets.extentions import debug
import os
current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(os.path.dirname(current_path))
working_dir = parent_path + "/settings.con"
print("settings file found at: " + working_dir)
def get(setting_name, location=working_dir):
    try:
        with open(location, "r") as f:
            for line in f:
                if setting_name in line:
                    name, value = [s.strip() for s in line.split("=")]
                    if value == "true":
                        return True
                    if value == "false":
                        return False
                    return value
    except Exception as error:
        pass
        #debug.report(f"failed to get setting '{setting_name}' from con file, this may cause the software to crash or hang. the error returned was: {error}")
              

def change(setting_name, new_value, location=working_dir):
    with open(location, "r") as file:
        lines = file.readlines()

        # Find the index of the specific line
        data = get(setting_name)
        if data is True:
            dvalue = "true"
        elif data is False:
            dvalue = "false"
        else:
             dvalue = get(setting_name)
        specific_line_index = lines.index(setting_name + " = " + dvalue + "\n")

        # Split the contents into three parts
        part1 = "".join(lines[:specific_line_index])
        part3 = "".join(lines[specific_line_index + 1:])
        new_setting = setting_name + " = " + new_value + "\n"

        # Re-assemble file
        file = open(location, "w")
        file.write(str(part1) + new_setting + str(part3))


