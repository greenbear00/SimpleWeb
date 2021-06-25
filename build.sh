#! /bin/bash
variable1=$0
variable2=${1:-$variable1}
# variable3=$2

echo $variable1, $variable2

if [[ $variable2 = *"build"* ]]; then
  echo "input argument [stop | start] [nifi=#number]"
elif [[ $variable2 = *"stop"* ]]; then
  echo "stop"
  docker-compose down
else
  echo "start...."

  
  
  echo "docker-compose up -d --build"
  docker-compose up -d --build
fi
