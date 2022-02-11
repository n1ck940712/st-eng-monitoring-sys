output=$(sshpass -p 'FlotechP@$$787814' ssh pi@192.168.1.6 "df -h | grep /media/pi") 
drive_name=${output##* }
# echo $drive_name

if ! [ -z "$output" ];
then
{
    for x in $FOO
    do
        # sshpass -p 'FlotechP@$$787814' scp "/home/pi/monitoring_sys/core/static/assets/reports/$x.pdf" pi@192.168.1.6:"/home/pi/monitoring_sys"
        sshpass -p 'FlotechP@$$787814' scp "/home/pi/monitoring_sys/core/static/assets/reports/$x.pdf" pi@192.168.1.6:"$drive_name"
    done
    echo -n 0
}
else {
    echo -n 2
}
fi