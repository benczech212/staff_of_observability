
SOURCE_ENV_FILE_PATH="staff_of_o11y.service"
TARGET_ENV_FILE_PATH="/etc/sysconfig/staff_of_o11y"
SOURCE_SERVICE_FILE_PATH="staff_of_o11y.service"
TARGET_SERVICE_FILE_PATH="/etc/systemd/system/staff_of_o11y.service"

# Create the environment file
echo "Creating environment file at $ENV_FILE_PATH"
cp $SOURCE_ENV_FILE_PATH $TARGET_ENV_FILE_PATH

# Create the service file
echo "Creating service file at $SERVICE_FILE_PATH"
cp $SOURCE_SERVICE_FILE_PATH $TARGET_SERVICE_FILE_PATH

# Start the service
echo "Starting staff_of_o11y service"
systemctl daemon-reload
systemctl enable staff_of_o11y
systemctl start staff_of_o11y
systemctl status staff_of_o11y

