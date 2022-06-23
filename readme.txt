docker run -it --rm --privileged tonistiigi/binfmt --install all
docker buildx build --platform linux/arm64,linux/amd64 . -t registry.local/wyze_sensor:v0.0.1 --push 
