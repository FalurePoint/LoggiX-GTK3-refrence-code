import subprocess

def convert_gtk3_to_gtk4(gtk3_file, gtk4_file):
    try:
        subprocess.run(['gtk2to3', gtk3_file, gtk4_file], check=True)
        print("Conversion completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Conversion failed:", e)

# Example usage
convert_gtk3_to_gtk4('gtk3.xml', 'gtk4.xml')
