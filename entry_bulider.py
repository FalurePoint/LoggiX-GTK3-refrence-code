import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Text Entry Example")

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry1 = Gtk.Entry()
        self.entry1.connect("activate", self.on_entry1_activate)
        vbox.pack_start(self.entry1, True, True, 0)

        self.entry2 = Gtk.Entry()
        self.entry2.connect("activate", self.on_entry2_activate)
        vbox.pack_start(self.entry2, True, True, 0)

        self.entry3 = Gtk.Entry()
        self.entry3.connect("activate", self.on_entry3_activate)
        vbox.pack_start(self.entry3, True, True, 0)

        button = Gtk.Button(label="Submit")
        button.connect("clicked", self.on_button_clicked)
        vbox.pack_start(button, True, True, 0)

    def on_entry1_activate(self, entry):
        self.entry2.grab_focus()

    def on_entry2_activate(self, entry):
        self.entry3.grab_focus()

    def on_entry3_activate(self, entry):
        self.on_button_clicked(None)

    def on_button_clicked(self, button):
        print("Button pressed")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
