echo This will remove LoggiX from your system

function uninstall {

echo "Removing LoggiX..."

rm -r ~/.local/share/applications/LoggiX


rm ~/Desktop/LoggiX-Development.desktop




clear
echo LoggiX removed
exit
}



while true; do
    read -p "Do you wish to uninstall this program? (Y/n)" yn
    case $yn in
        [Yy]* ) uninstall; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
