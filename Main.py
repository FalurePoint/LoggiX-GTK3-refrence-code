# Import extra scripts from extention folder
from assets.extentions import *

# import Gtk
import gi
import webbrowser
import os

# Require Gtk3+ and import it as "gtk"
gi.require_version('Gtk', "3.0")
from gi.repository import Gtk as gtk

# Global variables
current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(os.path.dirname(current_path))
gui_files = parent_path + "/LoggiX/assets/UI/LoggiX_UI_2.0.XML"
log_path = parent_path + "/LoggiX/assets/contacts.hlf"

# software version globals
application_version = "1.0 Beta"
LoTw_connect_version = "N/A"
QRZ_connect_version = "N/A"

# predefine globals
veiw_page_root = 1
starting_page_number = 1
max_lines = 65
global_display_string = ""


# Opens the log file and returns the content and line totals in [0] and [1] respectively
def read_logs():
    log_file = open(log_path, "r")  # get the content
    log_data = log_file.read()
    log_file.close()
    with open(log_path, 'r') as f:  # get the line totals
        line_count = 0
        for line in f:
            line_count += 1
    return log_data, line_count


# Main class contains most of the code for the application
class LoggixMain:
    # Init or initialize is exactly what it sounds like, it initializes the gui and other major features
    def __init__(self):
        global gui_files

        # Begin GTK
        self.builder = gtk.Builder()
        self.builder.add_from_file(gui_files)
        self.builder.connect_signals(self)

        # Get all the GUI objects
        self.get_objects_update()

        # Set the main window title.
        self.gui_title_banner.set_text(f"LoggiX {application_version} GitHub Nightly")

        # set initial page number for the gui, it's always one...
        self.gui_current_page.set_text(" 1 ")
        self.gui_total_pages.set_text(str(self.calculate_pages(read_logs()[0])))

        # Write the log file to the global variable that the GUI text output for the log reads from and update.
        self.global_display_is(read_logs()[0])
        self.update_log_output(display_range=True, top=max_lines)

        # Begin main window and connect close signal from GUI.
        window = self.gui_main_window
        window.connect("delete-event", gtk.main_quit)
        window.show()

    #  refresh data avalible from the gui (will not update gui output widgets)
    def get_objects_update(self):
        # Title
        self.gui_title_banner = self.builder.get_object("title_banner")
        self.gui_title_options_button = self.builder.get_object("title_bar_options_button")

        # Main GUI
        self.gui_main_window = self.builder.get_object("loggix_gui_main")
        self.gui_input_time = self.builder.get_object("input_time")
        self.gui_input_date = self.builder.get_object("input_date")
        self.gui_input_freq = self.builder.get_object("input_freq")
        self.gui_input_callsign = self.builder.get_object("input_callsign")
        self.gui_input_power = self.builder.get_object("input_power")
        self.gui_input_mode = self.builder.get_object("input_mode")
        self.gui_input_report = self.builder.get_object("input_report")
        self.gui_input_comment = self.builder.get_object("input_comment")
        self.gui_main_display = self.builder.get_object("gui_main_display")
        self.gui_search_input = self.builder.get_object("nav_search_entry")
        self.gui_search_button = self.builder.get_object("nav_search_button")
        self.gui_next_page = self.builder.get_object("nav_next_button")
        self.gui_last_page = self.builder.get_object("nav_last_button")
        self.gui_current_page = self.builder.get_object("nav_page_display_one")
        self.gui_total_pages = self.builder.get_object("nav_page_display_two")

        # options dropdown
        self.gui_options_dropdown = self.builder.get_object("options_dropdown")
        self.gui_debug_mode = self.builder.get_object("debug_mode_toggle")
        self.gui_setting_button = self.builder.get_object("options_settings_button")
        self.gui_contribue_button = self.builder.get_object("options_contribute_button")
        self.gui_website_button = self.builder.get_object("options_website_button")
        self.gui_about_button = self.builder.get_object("options_about_button")
        self.gui_version_notice = self.builder.get_object("options_gui_version_lable")

    # lots of little empty calls at the moment, GUI elements are connected though
    def show_options(self, dummy):
        self.gui_options_dropdown.show_all()

    def about_software(self, dummy):
        About()

    def settings_gui(self, dummy):
        SettingsMenu()

    def add_log_file(self, dummy):
        NewLogWindow()

    def open_website(self, dummy):
        webbrowser.open("https://qsl.net/kl5is")

    # devides the total lines buy the amount of lines allow per page defined by the global "max_lines"
    def calculate_pages(self, input_data, dummy=None):
        string_lines = len(input_data.split('\n'))  # find total lines in string by breaking at \n
        if string_lines < max_lines:  # less then one is over-ridden and 1 is used instead because you can't have data AND 0 pages... :P
            return " 1 "
        else:
            pages = int(string_lines) // max_lines
            pages = pages + 1
            pages = " " + str(pages) + " "
            return pages

    # pushes new data to self.gui_main_display from a supplyed string or directly from the current .hlf file being used
    def update_log_output(self, content=None, display_range=False, bottom=1, top=max_lines):  # used to write data to the log textveiw in gui, capable of writing a string or pulling from log file.
        global global_display_string
        log_buffer = self.gui_main_display.get_buffer()
        if content is None:  # no string was passed (strings have priority)
            self.gui_total_pages.set_text(self.calculate_pages(str(global_display_string)))
            if display_range is True:
                log_buffer.set_text(get_range.get_from_string(global_display_string, bottom, top))
            else:
                log_buffer.set_text(global_display_string)
        else:  # a string was passed
            self.gui_total_pages.set_text(self.calculate_pages(str(content)))
            if display_range is True:
                log_buffer.set_text(get_range.get_from_string(content, bottom, top))  # write to log output with range
            else:
                log_buffer.set_text(content)

    # by defining output as a variable it can be temparaly over-written to alow displaying things such as search resaults from user log search.
    def global_display_is(self, input_data):
        global global_display_string
        global_display_string = input_data

    # gets any new information from text entrys.
    def update_inputs(self):
        time = self.gui_input_time.get_text().strip()
        date = self.gui_input_date.get_text().strip()
        freq = self.gui_input_freq.get_text().strip()
        call = self.gui_input_callsign.get_text().strip()
        power = self.gui_input_power.get_text().strip()
        mode = self.gui_input_mode.get_text().strip()
        report = self.gui_input_report.get_text().strip()
        comment = self.gui_input_comment.get_text().strip()
        search_querry = self.gui_search_input.get_text().strip()
        print("Update to builder input objects finished")
        return time, date, freq, call, power, mode, report, comment, search_querry

    # Adds an entry to the log file, currently lacking. Todo: prepend to log,  finish incomplete entry detect, watts slot autofill improvement.
    def add_to_log(self, dummy):
        values = self.update_inputs()  # stores the data from get_inputs() in value for unpacking in line 177
        if values:
            value_id = 0
            incomplete_detect = False
            while value_id <= 6:
                if values[value_id] != "":
                    print("found content in field ", value_id)
                    value_id = value_id + 1
                else:
                    value_id = 7
                    incomplete_detect = True
                    gui_addons.Warning()
                    print("well i tried...")
            if incomplete_detect is False:
                log_entry = f"\n{values[0]} | {values[1]} | {values[2]} | {values[3]} | {values[4].replace('w', '').replace('W', '')}w | {values[5]} | {values[6]} | {values[7]}\n"  # unpackes then compiles to a log entry line
                log_file = open(log_path, 'a')  # opens the log and writes the data to the log file
                log_file.write(str(log_entry))
                log_file.close()
                self.page_adjust("reset")
                self.global_display_is(read_logs()[0])
                self.update_log_output(display_range=True, top=max_lines)  # update gui

    # parse the log file for lines containing the search term and update the data passed to self.main_display
    def search_logs(self, dummy):
        search_input = self.update_inputs()
        search_input = f"{search_input[8]}"  # unpack the searchbox from get_inputs()
        if search_input == "":  # if an empty search is initiated then return to main log
            self.global_display_is(read_logs()[0])
            self.update_log_output(display_range=True, top=max_lines)
        else:
            total_lines = read_logs()[1]  # get total lines
            working_line = 0
            search_output = ""  # clear the output for a fresh search
            while working_line < total_lines:  # parse each line for search resualts
                resaults = search_function.line_has(log_path, working_line, str(search_input))  # if this line has
                if resaults is True:
                    search_output = search_output + str(search_function.get_line(log_path, working_line + 1))  # append new resaults from each positive line to the resault string
                working_line = working_line + 1
            self.global_display_is(search_output)
            self.update_log_output(display_range=True, top=max_lines)  # update the gui

    # based on input it calulates what range if lines to display to move forware or back a "page:
    def page_adjust(self, move):  # Change current page in gui to +1 or -1 based on input
        global veiw_page_root
        global starting_page_number
        current_page = self.builder.get_object("active_page")
        if move == "next":
            starting_page_number = starting_page_number + 1
            self.gui_current_page.set_text(" " + str(starting_page_number) + " ")
        if move == "prev":
            starting_page_number = starting_page_number - 1
            self.gui_current_page.set_text(" " + str(starting_page_number) + " ")
        if move == "reset":
            veiw_page_root = 1
            starting_page_number = 1
            self.gui_current_page.set_text(" " + str(starting_page_number) + " ")

    # calls page_adjust corectly for forward one and updates self.gui_current_page.
    def next_page(self, dummy):  # Shift  veiw range up one page
        global veiw_page_root
        bottom_of_page = len(global_display_string.split('\n'))
        if veiw_page_root + max_lines - 2 < bottom_of_page:
            veiw_page_root = veiw_page_root + max_lines
            self.update_log_output(display_range=True, bottom=veiw_page_root, top=veiw_page_root + max_lines)
            self.page_adjust("next")

    # calls page_adjust corectly for backward one and updates self.gui_current_page.
    def last_page(self, dummy):  # Shift veiw range down one page
        global veiw_page_root
        if veiw_page_root - max_lines > -1:
            veiw_page_root = veiw_page_root - max_lines
            self.update_log_output(display_range=True, bottom=veiw_page_root, top=veiw_page_root + max_lines)
            self.page_adjust("prev")


# about software screen main class TODO: fix window not "sticking" to center of main window
class About:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(gui_files)  # start the GTK Bulider and load the gui file
        self.loggix_about_main = self.builder.get_object("loggix_about")  # initiate gui window and display
        self.loggix_about_main.connect("delete-event", self.kill)
        self.loggix_about_main.show()

    def kill(self, dummy1, dummy2):
        self.loggix_about_main.get_toplevel().destroy()


# settings menu main class (Unfinished LOW priority).
class SettingsMenu:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(gui_files)  # start the GTK Bulider and load the gui file
        self.loggix_about_main = self.builder.get_object("settings_window")  # initiate gui window and display
        self.loggix_about_main.connect("delete-event", self.kill)
        self.loggix_about_main.show()

    def kill(self, dummy1, dummy2):
        self.loggix_about_main.get_toplevel().destroy()


# new file dialogue for opening/starting logs main class (Unfinished LOW priority).
class NewLogWindow:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(gui_files)  # start the GTK Bulider and load the gui file
        self.loggix_about_main = self.builder.get_object("new_log_window")  # initiate gui window and display
        self.loggix_about_main.connect("delete-event", self.kill)
        self.loggix_about_main.show()

    def kill(self, dummy1, dummy2):
        self.loggix_about_main.get_toplevel().destroy()


if __name__ == '__main__':
    main = LoggixMain()
    gtk.main()
