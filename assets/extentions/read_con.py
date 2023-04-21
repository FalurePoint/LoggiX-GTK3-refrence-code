from assets.extentions import debug
import os
current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(os.path.dirname(current_path))
working_dir = parent_path + "/settings.con"
print(working_dir)
def get(setting_name, location=working_dir):
    try:
        with open(location, "r") as f:
            for line in f:
                if setting_name in line:
                    name, value = [s.strip() for s in line.split("=")]
                    return value
    except Exception as error:
        debug.report(f"failed to get setting '{setting_name}' from con file, this may cause the software to crash or hang. the error returned was: {error}")
              