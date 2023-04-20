# LoggiX install shell script

echo Welcome to the LoggiX command line installer for LoggiX version 1.0 Beta!


# function to install LoggiX
function install {

echo "Installing LoggiX..."
mkdir ~/.local/share/applications/LoggiX
cp Main.py ~/.local/share/applications/LoggiX
cp -r assets ~/.local/share/applications/LoggiX

cd ~/.local/share/applications
touch LoggiX-Development.desktop
echo  [Desktop Entry] >> LoggiX-Development.desktop
echo  Version=1.0 >> LoggiX-Development.desktop
echo  Type=Application >> LoggiX-Development.desktop
echo  Terminal=false >> LoggiX-Development.desktop
echo  Exec=python3 ~/.local/share/applications/LoggiX/Main.py >> LoggiX-Development.desktop
echo  Name=LoggiX Development Beta >> LoggiX-Development.desktop
echo  Icon=~/.local/share/applications/LoggiX/assets/logo/loggix_icon.png >> LoggiX-Development.desktop
gio set ~/.local/share/applications/LoggiX-Development.desktop metadata::trusted true
chmod a+x ~/.local/share/applications/LoggiX-Development.desktop
chmod a+x ~/.local/share/applications/LoggiX/Main.py
#clear
}

function add_to_desktop {
touch ~/Desktop/LoggiX-Development.desktop
echo  [Desktop Entry] >> ~/Desktop/LoggiX-Development.desktop
echo  Version=1.0 >> ~/Desktop/LoggiX-Development.desktop
echo  Type=Application >> ~/Desktop/LoggiX-Development.desktop
echo  Terminal=false >> ~/Desktop/LoggiX-Development.desktop
echo  Exec=python3 ~/.local/share/applications/LoggiX/Main.py >> ~/Desktop/LoggiX-Development.desktop
echo  Name=LoggiX Development Beta >> ~/Desktop/LoggiX-Development.desktop
echo  Icon=~/.local/share/applications/LoggiX/assets/logol/loggix_icon.png >> ~/Desktop/LoggiX-Development.desktop
gio set ~/Desktop/LoggiX-Development.desktop metadata::trusted true
chmod a+x ~/Desktop/LoggiX-Development.desktop
}


# confirm whether to install or not
while true; do
    read -p "Do you wish to install this program? (Y/n)" yn
    case $yn in
        [Yy]* ) install; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

while true; do
    read -p "Do you want this added to your desktop as well? (Y/n)" yn
    case $yn in
        [Yy]* ) add_to_desktop; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "LoggiX installed"
exit
