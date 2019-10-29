#! /bin/bash

# http://woowabros.github.io/tools/2017/08/17/ost_bash.html
# 실행된 쉘 스크립트의 절대 경로를 가져옵니다.
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  TARGET="$(readlink "$SOURCE")"
  if [[ $SOURCE == /* ]]; then
    SOURCE="$TARGET"
  else
    DIR="$( dirname "$SOURCE" )"
    SOURCE="$DIR/$TARGET"
  fi
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

BASEDIR=$DIR

IFS="/"
BASEDIR_SPLIT=($BASEDIR)
IFS=""

# Root 디렉토리를 구합니다.
GEMS_HOME=""

for key in "${!BASEDIR_SPLIT[@]}";
    do {
        if [[ $key > 0 && $key < $(( ${#BASEDIR_SPLIT[@]} - 2 )) ]]; then
            GEMS_HOME="$GEMS_HOME""/""${BASEDIR_SPLIT[$key]}"
        fi;
    };
done

# bash_profile에 PATH를 추가해줍니다.
echo "export GEMS_HOME=$GEMS_HOME" >> ~/.bash_profile
echo "export PATH=$PATH:$GEMS_HOME" >> ~/.bash_profile

echo "Root directory is $GEMS_HOME"
# 끝!
echo "Done!"
