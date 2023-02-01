!/bin/bash
#
#   build.sh: script will run the subscriber "behind" docker
#
docker build . -t fcosfc/mqtt-client
docker login
docker push fcosfc/mqtt-client