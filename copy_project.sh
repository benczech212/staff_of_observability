HOSTNAME=192.168.4.104
USERNAME=ben
SOURCE_PATHS=( "../staff_of_observability/python_client")
REMOTE_PATH=/home/ben/dev/staff_of_observability
RESTART_SERVICE=true
if [ "$1" == "--restart" ]; then
    RESTART_SERVICE=true
fi
# until ping -c 1 $HOSTNAME &>/dev/null; do
#     echo "Waiting for $HOSTNAME to be reachable..."
#     sleep 5
# done


# until ping -c 1 $HOSTNAME &>/dev/null; do
#     echo "Waiting for $HOSTNAME to be reachable..."
#     sleep 2
# done
for SOURCE_PATH in "${SOURCE_PATHS[@]}"
do
    echo "Copying $SOURCE_PATH to $HOSTNAME:$REMOTE_PATH"
    sudo scp -r $SOURCE_PATH $USERNAME@$HOSTNAME:$REMOTE_PATH
done
if [ "$RESTART_SERVICE" = true ]; then
    echo "Restarting service on $HOSTNAME"
    ssh $USERNAME@$HOSTNAME 'sudo systemctl restart staff_of_o11y'
fi
