import gi
import os
current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(os.path.dirname(current_path))
missing_data_gui = parent_path + "/UI/Missing_data_warning.XML"
gi.require_version('Gtk', "3.0")
from gi.repository import Gtk as gtk  # Require Gtk3+ and import it as "gtk"

cancel = False
continue_anyway = False

class Warning:

    def __init__(self):
        global cancel
        global continue_anyway
        cancel = False
        continue_anyway = False
        global missing_data_gui
        self.builder = gtk.Builder()
        self.builder.add_from_file(missing_data_gui)  # start the GTK Bulider and load the gui file
        self.builder.connect_signals(self)  # connect the hooks to there respective functions
        self.window = self.builder.get_object("Main")  # initiate gui window and display
        self.window.connect("delete-event", self.cancel)
        self.window.show()

    def cancel(self, dummy, close_dummy=None):
        global cancel
        self.window.get_toplevel().destroy()
        cancel = True

    def continue_anyway(self, dummy):
        global continue_anyway
        self.window.get_toplevel().destroy()
        continue_anyway = True


if __name__ == '__main__':
    about = About()
    warning = Warning()
    test = Test()
    gtk.main()
