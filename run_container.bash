
xhost +local:docker

#Capture the current working directory
cwd=$(pwd)

docker run -it \
    --name vision_container \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix" \
    --net=host \
    --privileged \
    --mount type=bind,source=$cwd/vot-workspace,target=/home/vot-workspace \
    vision-vot \
    bash
    
docker rm vision_container
    
    
