

cirpy_env_path=~/cirpy_env
cirpy_env_name=cirpy

echo "Setting up cirpy environment"

# Setup project
python3 -m venv $cirpy_env_path/$cirpy_env_name

# Add aliases to ~/.bashrc
echo "alias cirpy='sudo $cirpy_env_path/$cirpy_env_name/bin/python3'" >> ~/.bashrc
echo "alias cirpypip='sudo $cirpy_env_path/$cirpy_env_name/bin/pip3'" >> ~/.bashrc

# Source ~/.bashrc to apply changes
source ~/.bashrc