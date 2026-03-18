#!/data/data/com.termux/files/usr/bin/bash

# Update package lists
apt update && apt upgrade -y

# Install Python and pip
apt install python python-pip -y

# Install required Python dependencies
pip install requests beautifulsoup4

# Environment Configuration
# Create a directory for the CC Checker if it does not exist
if [ ! -d "$HOME/CCChecker" ]; then
    mkdir $HOME/CCChecker
fi

# Message to the user
echo "CC Checker setup is complete! You can find it in ~/CCChecker."