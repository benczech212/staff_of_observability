HOSTNAME=192.168.4.99
USERNAME=ben
SOURCE_PATH="../staff_of_observability/*"
REMOTE_PATH=/home/ben/dev/staff_of_observability

# until ping -c 1 $HOSTNAME &>/dev/null; do
#     echo "Waiting for $HOSTNAME to be reachable..."
#     sleep 5
# done


# until ping -c 1 $HOSTNAME &>/dev/null; do
#     echo "Waiting for $HOSTNAME to be reachable..."
#     sleep 2
# done
scp -r $SOURCE_PATH $USERNAME@$HOSTNAME:$REMOTE_PATH