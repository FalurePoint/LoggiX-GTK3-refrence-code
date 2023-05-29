# Import extra scripts from extention folder
import test_variables
from assets.extentions import *
debug.report("Loading new instance...", display_location=False)
# import modules
try:
    import gi
    import webbrowser
    import os
    from datetime import datetime
    import time
except Exception as error:
    debug.report(f"Failed to import required modules exiting with: {error}", display_location=False)
    exit(1)


# Require Gtk3+ and import it as "gtk"
debug.report("setting GTK requirements...", display_location=False)
try:
    gi.require_version('Gtk', "3.0")
    from gi.repository import Gtk as gtk
    from gi.repository import Gdk as gdk
    debug.report("GTK ready...", display_location=False)
except Exception as error:
    debug.report(f"Failed to set GTK requrements exiting with error: {error}", display_location=False)
    exit(1)


# TODO-------------------Global path locations------------------TODO
# Global file paths

# settings globals
debug.report("Loading settings file...", display_location=False)
try:
    dupe_checking = read_con.get("dupe_checking")
    qs_dropdowns = read_con.get("contest_qsd")
    default_contest = read_con.get("contest_mode_on_startup")
    display_welcome = read_con.get("show_welcome_message")
    log_path = read_con.get("current_log")
except Exception as error:
    debug.report(f"Failed to load settings from file... error: {error}")
    debug.report("Software closing with dignity.")
    exit()

if display_welcome:
    read_con.change("current_log", f"/home/{os.getlogin()}/.local/share/applications/LoggiX/assets/contacts.hlfv2")
    log_path = read_con.get("current_log")

debug.report("Connecting globals...", display_location=False)
try:
    current_path = os.path.abspath(__file__)
    parent_path = os.path.dirname(os.path.dirname(current_path))

    gui_files = parent_path + "/LoggiX/assets/UI/LoggiX_UI_2.0.XML"
    debug.report("4", display_location=False)
    hlfio.set_log(log_path)
    hlfio.validate_file()


    # software version globals
    application_version = "1.4.4"
    LoTw_connect_version = "N/A"
    QRZ_connect_version = "N/A"

    # predefine globals
    contest_mode_state = False
    veiw_page_root = 1
    starting_page_number = 1
    max_lines = 65
    global_display_string = ""
except Exception as error:
    debug.report(f"Failed to predefine globals. error: {error}", display_location=False)
    if "[Errno 2] No such file or directory" in str(error):
        debug.report('This might be due to an invalid file path in your settings file. are they all correct?', display_location=False)
    debug.report("Software closing with dignity.", display_location=False)
    exit()


# Opens the log file and returns the content and line totals in [0] and [1] respectively
def read_logs(location=log_path):
    try:
        with open(location, 'r') as f:  # get the line totals
            line_count = 0
            final_output = ""
            for line in f:
                line_count += 1
                hreadable = hlfio.create_human_readable(line_count)
                if hreadable != "!EMPTY!":
                    final_output = str(final_output) + str(hreadable) + "\n \n"
        return final_output, line_count
    except Exception as error:
        debug.report(f"Failed to open Log file! error: {error}")

debug.report("Finished main class preamble...", display_location=False)

# Main class contains most of the code for the application
class LoggixMain:
    global log_path
    # Init or initialize is exactly what it sounds like, it initializes the gui and other major features
    def __init__(self):
        debug.report("Starting Class LoggixMain()...", display_location=False)
        try:
            global gui_files

            # Begin GTK
            self.builder = gtk.Builder()
            self.builder.add_from_file(gui_files)
            self.builder.connect_signals(self)

            # Get all the GUI objects
            self.get_objects_update()

            # Set the main window title.
            self.gui_title_banner.set_text(f"LoggiX {application_version}")

            # force contest mode if the contest_mode_on_startup is true
            if default_contest:
                self.gui_options_contest_mode.set_active(True)
                self.contest_mode_init("dummy")

            if display_welcome:
                # show the welcome message for the current version of LoggiX
                self.display_welcome()
                read_con.change("show_welcome_message", "false")
            else:
                # Write the log file to the global variable that the GUI text output for the log reads from and update.
                self.global_display_is(read_logs()[0])
                self.update_log_output(display_range=True, top=max_lines)

            # set initial page number for the gui, it's always one...
            self.gui_loggix_current_page.set_text(" 1 ")
            self.gui_loggix_total_pages.set_text(str(self.calculate_pages(read_logs()[0])))


            # Begin main window and connect close signal from GUI.
            window = self.gui_loggix_main_window
            window.connect("delete-event", gtk.main_quit)
            window.connect("key_press_event", self.shortcut_detect)
            window.show()




            # Report to log that we made it through Initialization without error.
            debug.report(f"Software started. Running from: {parent_path}/LoggiX", display_location=False)
            debug.newline()

        except Exception as error:
            debug.report(f"Initialization error: {error} \n A controlled shutdown was preformed...")
            print("Failed to initialize software... Exit code: 1")
            exit(1)

    def display_welcome(self):
        message = f"""

        Hello! Welcome to loggix {application_version}!
        This is the GTK3 1.0 design of LoggiX which I am abandoning and moving to a more modern build\
        with GTK4 and Gnome Builder layout in favour of being a more usable and integrated software\
        However even though this software is not usable in production yet, in the hopes of wetting the lips of the Linux\
        Ham community at large and getting some feedback and maybe even some help on the GTK4 version when the base port is released.\
        So feel free to look around! \
        If you are interested in helping out (Or know anything at all about developing modern Gnome apps with Builder) you can reach out to me at:\
        KL5IS@protonmail.com\
        KL5IS@qsl.net\
        \
        THIS MESSAGE WILL ONLY SHOW ONCE! HIT ESC TO CLOSE IT.\
        WARNING: this software is not ready to be used and the GTK3 version probably never will.\
        Please do not try to use this in contesting... The Cabrillo export function is unfinished and will not work right it will end up embeding\
        data about me rather then you in your log and it is quite a complex repair.\
        \
        \
        The latest release notes (from before archiving the GTK3 version) are below:\
        \
         1.4.4 UPDATE NOTICE: cabrillo logs have been introduced for testing but are not funtional yet as they will assume test data for use instead of getting real user info.

          1. Improved duplicate checking including both exact AND similar detection systems
          2. Log format migration to hlf version 2.1 with improved access speeds allowing log sizes up to 1500 entrys before experiencing access lag!
          3. Double click quick settings drop downs for frequncy, power, and mode
          4. Settings functionality in settings file (the settings GUI is still unfinished though)
          5. Log search moved to the context menu to be more out of the way
          6. Date/time auto detect is UTC instead of local time now (sorry about that)
          7. updated about/credits window (Josh, you may want to take a look at it!)



        Now due to the fact that I am at the moment working though a lot of school, including learning two new programing
        languages in addition to python, learning data analysis, and training for a ETT licence over the summer this software is still missing a few vital features
        that you will want to know before using it.

          1. THERE IS NO WAY TO EXPORT A CABRILLO LOG FILE (functionaly) YET! probably the bigest issue at the moment.
          2. the settings GUI is not functional yet
          3. it has no sync funtionality to qrz or LoTw at the moment
          4. creating a new log file manualy is the only way to make a new log.


        As said above, this is a WIP all these issues DO have fixes planed with most of them already in the works.
        The only thing missing is time and help.
        if you have experience with python or Gnome's GTK3 design system and like this project the best thing you can possably donate is a little bit
        of your time and skill to help me get this project up to a "Big gun" worthy compition tool!
        if your willing send me an email at KL5IS@qsl.net


        Thanks for trying up my project! -Ace, KL5IS"""
        self.calculate_pages(force_size="5")
        self.global_display_is(message)
        self.update_log_output()

    def update_time(self):
        current_utc = str(datetime.utcnow())
        self.gui_loggix_input_time.set_text(current_utc)


    def shortcut_detect(self, widget, event):
        if event.keyval == gdk.KEY_Control_R:
            self.global_display_is(read_logs()[0])
            self.update_log_output(display_range=True, top=max_lines)
            self.gui_loggix_input_callsign.grab_focus()
            return True
        if event.keyval == gdk.KEY_Escape:
            self.gui_loggix_input_callsign.grab_focus()
            self.gui_loggix_input_callsign.set_text("")
            self.global_display_is(read_logs()[0])
            self.update_log_output(display_range=True, top=max_lines)
            return True

    #  refresh data avalible from the gui (will not update gui output widgets)
    def get_objects_update(self):
        try:
            # Title
            self.gui_title_banner = self.builder.get_object("title_banner")
            self.gui_title_options_button = self.builder.get_object("title_bar_options_button")

            # Main GUI
            self.gui_loggix_main_window = self.builder.get_object("loggix_gui_main")
            self.gui_loggix_input_time = self.builder.get_object("input_time")
            self.gui_loggix_input_date = self.builder.get_object("input_date")
            self.gui_loggix_input_freq = self.builder.get_object("input_freq")
            self.gui_loggix_input_callsign = self.builder.get_object("input_callsign")
            self.gui_loggix_input_power = self.builder.get_object("input_power")
            self.gui_loggix_input_mode = self.builder.get_object("input_mode")
            self.gui_loggix_input_report = self.builder.get_object("input_report")
            self.gui_loggix_input_comment = self.builder.get_object("input_comment")
            self.gui_loggix_comment_lable = self.builder.get_object("inputs_lable_comment")
            self.gui_loggix_input_time = self.builder.get_object("input_time")
            self.gui_loggix_main_display = self.builder.get_object("gui_main_display")
            self.gui_loggix_next_page = self.builder.get_object("nav_next_button")
            self.gui_loggix_last_page = self.builder.get_object("nav_last_button")
            self.gui_loggix_current_page = self.builder.get_object("nav_page_display_one")
            self.gui_loggix_total_pages = self.builder.get_object("nav_page_display_two")
            self.gui_loggix_serial_input = self.builder.get_object("nav_serial_entry")
            self.gui_loggix_local_serial = self.builder.get_object("nav_serial_number_display")
            self.gui_loggix_log_button = self.builder.get_object("nav_log_it_button")

            # options dropdown
            self.gui_options_dropdown_main = self.builder.get_object("options_dropdown")
            self.gui_options_power_dropdown = self.builder.get_object("power_dropdown")
            self.gui_options_mode_dropdown = self.builder.get_object("mode_dropdown")
            self.gui_options_band_dropdown = self.builder.get_object("band_dropdown")
            self.gui_options_contest_mode = self.builder.get_object("contest_mode_toggle")
            self.gui_options_setting_button = self.builder.get_object("options_settings_button")
            self.gui_options_contribue_button = self.builder.get_object("options_contribute_button")
            self.gui_options_website_button = self.builder.get_object("options_website_button")
            self.gui_options_about_button = self.builder.get_object("options_about_button")
            self.gui_options_search_input = self.builder.get_object("options_log_search_entry")
            self.gui_options_search_button = self.builder.get_object("options_log_search_button")
            self.gui_options_version_notice = self.builder.get_object("options_gui_version_lable")

            # settings window
            self.gui_settings_open_debug_button = self.builder.get_object("settings_header_debug_button")

            # debug tools
            self.debug_refresh_display = self.builder.get_object("debug_input_force_refresh")
            self.debug_flush_crash_log = self.builder.get_object("debug_input_flush_crash_reports")
            self.debug_flush_contact_log = self.builder.get_object("debug_input_flush_qso_log")
            self.debug_window_title = self.builder.get_object("debug_window_title")


        except Exception as error:
            debug.report(f"An exception was caught and ignored while connecting to GUI but is being logged just in case: {error}")
            print("WARNING: reported unhandeled error while connecting to GUI to debug log, you might want to look in to this...")

    # lots of little empty calls at the moment, GUI elements are connected though TODO: finish making, add debuging.
    def open_log_file(self):
        dialog = Gtk.FileChooserDialog(title="Save File", parent=self.gui_loggix_main_window, action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cab_file = dialog.get_filename().strip()
            cab_extention_check = cab_file[-4:]
            if cab_extention_check != ".log":
                cab_file = cab_file + ".log"
            cabrillo_write.begin_cabrillo(test_variables.user_data, cab_file)
            cabrillo_write.write_cabrillo(cab_file)
        dialog.destroy()



    def about_software(self, dummy):
        About()

    def open_debug_window(self):
        debug_tools()

    def settings_gui(self, dummy):
        SettingsMenu()

    def add_log_file(self, dummy):
        self.open_log_file()

    def open_website(self, dummy):
        webbrowser.open("https://qsl.net/kl5is")

    # devides the total lines buy the amount of lines allow per page defined by the global "max_lines"
    def calculate_pages(self, input_data=None, dummy=None, force_size=None):
        try:
            if force_size != None:
                pages = " " + str(force_size) + " "
                return pages
            string_lines = len(input_data.split('\n'))  # find total lines in string by breaking at \n
            if string_lines < max_lines:  # less then one is over-ridden and 1 is used instead because you can't have data AND 0 pages... :P
                return " 1 "
            else:
                string_lines = len(input_data.split('\n'))  # find total lines in string by breaking at \n
                pages = int(string_lines) // max_lines
                pages = pages + 1
                pages = " " + str(pages) + " "
                return pages
        except Exception as error:
            debug.report(f"Non-fatal error while trying to calculate total pages for GUI do display: {error}")

    # pushes new data to self.gui_main_display from a supplyed string or directly from the current .hlf file being used
    def update_log_output(self, content=None, display_range=False, bottom=1, top=max_lines):  # used to write data to the log textveiw in gui, capable of writing a string or pulling from log file.
        global global_display_string
        log_buffer = self.gui_loggix_main_display.get_buffer()
        if content is None:  # no string was passed (strings have priority)
            self.gui_loggix_total_pages.set_text(self.calculate_pages(str(global_display_string)))
            if display_range is True:
                log_buffer.set_text(get_range.get_from_string(global_display_string, bottom, top))
            else:
                log_buffer.set_text(global_display_string)
        else:  # a string was passed
            self.gui_loggix_total_pages.set_text(self.calculate_pages(str(content)))
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
        time = self.gui_loggix_input_time.get_text().strip()
        date = self.gui_loggix_input_date.get_text().strip()
        freq = self.gui_loggix_input_freq.get_text().strip()
        call = self.gui_loggix_input_callsign.get_text().strip()
        power = self.gui_loggix_input_power.get_text().strip()
        mode = self.gui_loggix_input_mode.get_text().strip()
        report = self.gui_loggix_input_report.get_text().strip()
        comment = self.gui_loggix_input_comment.get_text().strip()
        search_querry = self.gui_options_search_input.get_text().strip()
        print("Update to builder input objects finished")
        return time, date, freq, call, power, mode, report, comment, search_querry

    def serial_id(self):
        if contest_mode_state:
            log_file = open(log_path, 'r')
            input_data = log_file.read()
            serial_base = int(len(input_data.split('\n')))
            self.gui_loggix_local_serial.set_text(str(int((serial_base))))

    # prepare the data avalible from the inputs for entering in the log TODO: massive code clean up! I lost trak of what is what before I finished!
    def prep_raw(self, values):
        raw = values[0], values[1], values[2], values[3], values[4], values[5] # fill in what is already in the corect format
        if "/" in values[6]: # if it is entered with a / spliting for hlfv2 is easy
            rxrst = values[6].split("/")[0]
            txrst = values[6].split("/")[1]
        elif values[6].len() == 6: # assume it is a RST if it has 6 digits and split at three
            rxrst = values[6][3:]
            txrst = values[6][:3]
        elif values[6].len() == 4: # if four then assume it is a RS report and split at two
            rxrst = values[6][3:]
            txrst = values[6][:3]
        else:
            debug.report("RST report format recognition failed. please submit it as RST/RST, RS/RS, RSTRST, or RSRS...")
            rxrst = "!-missing-!"
            txrst = "!-missing-!"
        raw = raw + (rxrst,) + (txrst,)
        if contest_mode_state:
            if values[7] == "":
                raw = raw + ("!-missing-!",) + ("!-missing-!",)
            else:
                raw = raw + ("!-missing-!",) + (values[7],)
            if self.gui_loggix_serial_input.get_text() == "":
                raw = raw + ("!-missing-!",)
            else:
                raw = raw + (self.gui_loggix_serial_input.get_text(),)
            if self.gui_loggix_local_serial.get_text() == "":
                raw = raw + ("!-missing-!",)
            else:
                raw = raw + (self.gui_loggix_local_serial.get_text(),)
        else:
            if values[7] == "":
                raw = raw + ("!-missing-!",) + ("!-missing-!",) + ("!-missing-!",) + ("!-missing-!",)
            else:
                raw = raw + values[7] + ("!-missing-!",) + ("!-missing-!",) + ("!-missing-!",)
        return raw

    # check for dupelicates contacts in the log file.
    def dupe_check(self):
        dupe_awesome = r"""
██████╗   ██╗      ██╗  ██████╗   ███████╗    ██╗
██╔═══██╗██║      ██ ║  ██╔══██╗ ██  ╔════╝    ██ ║
██║      ██║██║      ██ ║  ██████╔╝█████╗         ██║
██║      ██║██║      ██ ║  ██╔═══╝    ██ ╔══╝          ╚═╝
██████╔╝ ╚██████╔╝  ██║            ███████╗  ██╗
╚══════╝       ╚═════╝      ╚═╝               ╚═══════╝   ╚═╝
"""
        if contest_mode_state:
            if dupe_checking:
                input_data = self.update_inputs()
                log_lenth = read_logs()[1]
                dupe_global = False

                # full check to see if a exact dupe exists.
                loopback = 0
                dupes = ""
                while loopback < log_lenth:
                    loopback += 1
                    if hlfio.get_raw(loopback) != "!EMPTY!":
                        if hlfio.get("freq", loopback) == input_data[2] and hlfio.get("callsign", loopback) == input_data[3]:
                            if hlfio.get("mode", loopback) == input_data[5] and hlfio.get("power", loopback) == input_data[4]:
                                dupe_global = True
                                dupes = dupes + hlfio.create_human_readable(loopback) + "\n"
                if dupe_global:
                    self.global_display_is(dupe_awesome + "\n\nDUPLICATE WARNING: Exact duplicates found!" + "\n \n" + dupes)
                    self.update_log_output(display_range=True, top=max_lines)

                #General use dupe check
                loopback = 0
                if not dupe_global:
                    while loopback < log_lenth:
                        loopback += 1
                        if hlfio.get_raw(loopback) != "!EMPTY!":
                            if hlfio.get("callsign", loopback) == input_data[3]:
                                dupe_global = True
                                dupes = dupes + hlfio.create_human_readable(loopback) + "\n"
                    if dupe_global:
                        self.global_display_is(dupe_awesome + " \n\nDUPLICATE WARNING! \nYou have other contacts with this station in your log from other bands/modes, please reveiw this before you continue to finalize this entry." + "\n \n" + dupes)
                        self.update_log_output(display_range=True, top=max_lines)

    # Adds an entry to the log file, currently lacking. TODO: finish incomplete entry detect.
    def add_to_log(self, dummy):
        if contest_mode_state: # set the passive clock time to current before writing to log
            utc = datetime.utcnow().time()
            utc = utc.strftime('%H:%M')
            self.gui_loggix_input_time.set_text(str(utc))
        values = self.update_inputs()  # stores the data from get_inputs() in value for unpacking in line 177
        if values:
            value_id = 0
            incomplete_detect = False
            while value_id <= 6:
                if values[value_id] != "":
                    value_id = value_id + 1
                else:
                    value_id = 7
                    incomplete_detect = True
                    gui_addons.Warning()

            if incomplete_detect is False:
                hlfio.write_to_log(self.prep_raw(values))
                self.serial_id()
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
                    search_output = search_output + str(hlfio.create_human_readable(working_line + 1)) + "\n" # append new resaults from each positive line to the resault string
                working_line = working_line + 1
            print(search_output)
            self.global_display_is(search_output)
            self.update_log_output(display_range=True, top=max_lines)  # update the gui

    # based on input it calulates what range if lines to display to move forware or back a "page:
    def page_adjust(self, move):  # Change current page in gui to +1 or -1 based on input
        global veiw_page_root
        global starting_page_number
        current_page = self.builder.get_object("active_page")
        if move == "next":
            starting_page_number = starting_page_number + 1
            self.gui_loggix_current_page.set_text(" " + str(starting_page_number) + " ")
        if move == "prev":
            starting_page_number = starting_page_number - 1
            self.gui_loggix_current_page.set_text(" " + str(starting_page_number) + " ")
        if move == "reset":
            veiw_page_root = 1
            starting_page_number = 1
            self.gui_loggix_current_page.set_text(" " + str(starting_page_number) + " ")

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

    def contest_mode_init(self, checkbutton_state):
        global contest_mode_state
        if self.gui_options_contest_mode.get_active():
            if hlfio.dataset() == "contesting":
                debug.report("contest mode enabled by user", display_location=False)
                contest_mode_state = True
                log_file = open(log_path, 'r')
                input_data = log_file.read()
                serial_base = len(input_data.split('\n'))
                self.gui_loggix_local_serial.set_text(str(int((serial_base - 1) / 2)))
                self.gui_loggix_serial_input.set_placeholder_text("TX Exchange here...")
                self.gui_loggix_input_date.set_text(str(datetime.utcnow().date()))
                utc = datetime.utcnow().time()
                utc = utc.strftime('%H:%M')
                self.gui_loggix_input_time.set_text(str(utc))
                self.gui_loggix_input_report.set_text("59/59")
                self.gui_loggix_input_freq.set_placeholder_text("double click for bands...")
                self.gui_loggix_input_power.set_placeholder_text("Enter contest power...")
                self.gui_loggix_input_mode.set_placeholder_text("Enter contest mode...")
                self.gui_loggix_comment_lable.set_text("RX exchange")
                self.serial_id()
            else:
                dialog = WarningDialog(self.gui_loggix_main_window, "WARNING: this log is not a contest log. please open a contest log or create a new one to switch to contesting mode.")
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    self.gui_options_contest_mode.set_active(False)
                    dialog.destroy()

        else:
            debug.report("contest mode disabled by user", display_location=False)
            self.gui_loggix_input_freq.set_placeholder_text("")
            self.gui_loggix_input_power.set_placeholder_text("")
            self.gui_loggix_input_mode.set_placeholder_text("")
            self.gui_loggix_local_serial.set_text("")
            self.gui_loggix_input_report.set_text("")
            self.gui_loggix_input_date.set_text("")
            self.gui_loggix_serial_input.set_placeholder_text("Contest mode is off...")
            self.gui_loggix_comment_lable.set_text("comment")

#TODO----------------Dropdowns----------------------TODO
    def show_options(self, dummy):
        self.gui_options_dropdown_main.show_all()
    def band_dropdown(self, dummy, dummy2):
        self.global_display_is(read_logs()[0])
        self.update_log_output(display_range=True, top=max_lines)
        if contest_mode_state:
            if qs_dropdowns:
                self.gui_options_band_dropdown.show_all()
    def power_dropdown(self, dummy, dummy2):
        self.global_display_is(read_logs()[0])
        self.update_log_output(display_range=True, top=max_lines)
        if contest_mode_state:
            if qs_dropdowns:
                self.gui_options_power_dropdown.show_all()
    def mode_dropdown(self, dummy, dummy2):
        self.global_display_is(read_logs()[0])
        self.update_log_output(display_range=True, top=max_lines)
        if contest_mode_state:
            if qs_dropdowns:
                self.gui_options_mode_dropdown.show_all()


#TODO--------------------misc GUI actions connect------------------------TODO
    def shift_comment(self, dummy):
            self.dupe_check()
            self.gui_loggix_input_comment.grab_focus()
    def shift_serial(self, dummy):
        if contest_mode_state:
            self.gui_loggix_serial_input.grab_focus()
    def shift_press_log(self, dummy):
        self.gui_loggix_log_button.clicked()
        self.gui_loggix_input_callsign.grab_focus()

    def band_select_70(self, band_option):
        self.gui_loggix_input_freq.set_text("420.000")
    def band_select_2(self, band_option):
        self.gui_loggix_input_freq.set_text("144.000")
    def band_select_6(self, band_option):
        self.gui_loggix_input_freq.set_text("50.000")
    def band_select_10(self, band_option):
        self.gui_loggix_input_freq.set_text("28.000")
    def band_select_20(self, band_option):
        self.gui_loggix_input_freq.set_text("14.000")
    def band_select_40(self, band_option):
        self.gui_loggix_input_freq.set_text("7.000")
    def band_select_80(self, band_option):
        self.gui_loggix_input_freq.set_text("3.500")
    def band_select_160(self, band_option):
        self.gui_loggix_input_freq.set_text("1.800")

    def power_select_5(self, band_option):
        self.gui_loggix_input_power.set_text("5W")
    def power_select_10(self, band_option):
        self.gui_loggix_input_power.set_text("10W")
    def power_select_50(self, band_option):
        self.gui_loggix_input_power.set_text("50W")
    def power_select_100(self, band_option):
        self.gui_loggix_input_power.set_text("100W")
    def power_select_200(self, band_option):
        self.gui_loggix_input_power.set_text("200W")
    def power_select_300(self, band_option):
        self.gui_loggix_input_power.set_text("300W")
    def power_select_500(self, band_option):
        self.gui_loggix_input_power.set_text("500W")
    def power_select_1500(self, band_option):
        self.gui_loggix_input_power.set_text("1500W")

    def mode_select_fm(self, band_option):
        self.gui_loggix_input_mode.set_text("FM")
    def mode_select_ssb(self, band_option):
        self.gui_loggix_input_mode.set_text("SSB")
    def mode_select_cw(self, band_option):
        self.gui_loggix_input_mode.set_text("CW")
    def mode_select_am(self, band_option):
        self.gui_loggix_input_mode.set_text("AM")
    def mode_select_ft8(self, band_option):
        self.gui_loggix_input_mode.set_text("FT8")
    def mode_select_rtty(self, band_option):
        self.gui_loggix_input_mode.set_text("RTTY")
    def mode_select_sstv(self, band_option):
        self.gui_loggix_input_mode.set_text("SSTV")
    def mode_select_data(self, band_option):
        self.gui_loggix_input_mode.set_text("DATA")


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

class debug_tools:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(gui_files)  # start the GTK Bulider and load the gui file
        self.loggix_debug_main = self.builder.get_object("debug_tools")  # initiate gui window and display
        self.loggix_debug_main.connect("delete-event", self.kill)
        self.loggix_debug_main.show()
        self.debug_refresh_display = self.builder.get_object("debug_input_force_refresh")
        self.debug_flush_crash_log = self.builder.get_object("debug_input_flush_crash_reports")
        self.debug_flush_contact_log = self.builder.get_object("debug_input_flush_qso_log")
        self.debug_window_title = self.builder.get_object("debug_window_title")
        self.debug_window_title.set_text(f"LoggiX {application_version} Debug tools (WARNING: these actions are unrestricted and ireversable you may damage you software/log data)")

    def kill(self, dummy1, dummy2):
        self.loggix_debug_main.get_toplevel().destroy()

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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class WarningDialog(Gtk.Dialog):
    def __init__(self, parent, message):
        Gtk.Dialog.__init__(self, "Warning", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        self.set_border_width(10)

        content_area = self.get_content_area()

        # Create the warning icon
        icon = Gtk.Image.new_from_icon_name("dialog-warning", Gtk.IconSize.DIALOG)

        # Create the label with the warning message
        label = Gtk.Label()
        label.set_text(message)

        # Add the icon and label to the dialog's content area
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.pack_start(icon, False, False, 0)
        box.pack_start(label, True, True, 0)
        content_area.add(box)

        self.show_all()



if __name__ == '__main__':
    main = LoggixMain()
    gtk.main()
