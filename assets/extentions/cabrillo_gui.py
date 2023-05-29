import gi
import os
gi.require_version('Gtk', "3.0")
from gi.repository import Gtk as gtk
page = 0

def grab_data():
    pass

class Main:
    def __init__(self):
        # Begin GTK
        self.builder = gtk.Builder()
        self.builder.add_from_file(f"{os.getcwd()}/UI/hlfv2cabrillo.XML")
        self.builder.connect_signals(self)

        # Begin main window and connect close signal from GUI.
        window = self.builder.get_object("cabrillo_create_gui_main_window")
        window.connect("delete-event", gtk.main_quit)
        window.show()
        
def inputs(self):
    email = self.builder.get_object("entry_email").get_text()
    address = self.builder.get_object("entry_address").get_text()
    location = self.builder.get_object("entry_location").get_text()
    mgl = self.builder.get_object("entry_mgl").get_text()
    name = self.builder.get_object("entry_name").get_text()
    callsign = self.builder.get_object("entry_callsign").get_text()
    contest = self.builder.get_object("entry_contest").get_text()
    club = self.builder.get_object("entry_club").get_text()
    comment = self.builder.get_object("entry_comment").get_text()
    
    overlay_combo = self.builder.get_object("combo_overlay")
    overlay_iter = overlay_combo.get_active_iter()
    if overlay_iter is not None:
        overlay = overlay_combo.get_model()[overlay_iter][0]
    else:
        overlay = None
        
    band_combo = self.builder.get_object("combo_band")
    band_iter = band_combo.get_active_iter()
    if band_iter is not None:
        band = band_combo.get_model()[band_iter][0]
    else:
        band = None
        
    mode_combo = self.builder.get_object("combo_mode")
    mode_iter = mode_combo.get_active_iter()
    if mode_iter is not None:
        mode = mode_combo.get_model()[mode_iter][0]
    else:
        mode = None
        
    power_combo = self.builder.get_object("combo_power")
    power_iter = power_combo.get_active_iter()
    if power_iter is not None:
        power = power_combo.get_model()[power_iter][0]
    else:
        power = None
        
    station_combo = self.builder.get_object("combo_station")
    station_iter = station_combo.get_active_iter()
    if station_iter is not None:
        station = station_combo.get_model()[station_iter][0]
    else:
        station = None
        
    opt_combo = self.builder.get_object("combo_opt")
    opt_iter = opt_combo.get_active_iter()
    if opt_iter is not None:
        opt = opt_combo.get_model()[opt_iter][0]
    else:
        opt = None
    
    return email, address, location, mgl, name, callsign, contest, club, comment, overlay, band, mode, power, station, opt

    def show_options(self, dummy, dummy2):
        print("done")
        self.builder.get_object("contest_select").show_all()
    
    def next(self, dummy):
        print("next")
        global page
        page = self.builder.get_object("notebook").get_current_page() + 1
        self.builder.get_object("notebook").set_current_page(page)
        
    
    def last(self, dummy):
        print("last")
        global page
        value = self.builder.get_object("notebook").get_current_page() - 1
        if value > (-1):
            page = value
        self.builder.get_object("notebook").set_current_page(page)
        
    def finish(self, dummy):
        print(self.inputs())

if __name__ == '__main__':
    main = Main()
    gtk.main()