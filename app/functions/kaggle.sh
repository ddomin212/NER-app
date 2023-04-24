first_time=$1
kernel_name=ner-app-kernel
if [ $first_time == "yes" ]; then
    kaggle datasets create -p app/static/generated/dataset
else
    kaggle datasets version -p app/static/generated/dataset -m '"new"'
fi

sleep 10

kaggle k push -p app/static/generated/kernel

kernel_status="running"
while [[ $kernel_status != "complete" ]]; do
    kernel_status=$(kaggle kernels status $kernel_name | grep -oP 'status "\K\w+')
    if [ $kernel_status == "error" ]; then
        echo "Kernel failed"
        break
    fi
    printf "Kernel status: $kernel_status"
    sleep 10
done

kaggle kernels output $kernel_name -p app/static/generated/output