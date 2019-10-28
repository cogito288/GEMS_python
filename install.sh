#! /bin/bash
# 윗 줄은 이 프로그램은 bash를 기반으로 실행된다는 뜻입니다.

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
SSPJ_HOME=""

for key in "${!BASEDIR_SPLIT[@]}";
	do {
		if [[ $key > 0 && $key < $(( ${#BASEDIR_SPLIT[@]} - 2 )) ]]; then
			SSPJ_HOME="$SSPJ_HOME""/""${BASEDIR_SPLIT[$key]}"
		fi;
	};
done

# bash_profile에 PATH를 추가해줍니다.
echo "export SSPJ_HOME=$SSPJ_HOME" >> ~/.bash_profile
echo "export PATH=$PATH:$SSPJ_HOME" >> ~/.bash_profile

echo "Root directory is $SSPJ_HOME"

# AWS CLI를 설치하기 위해 pip를 먼저 설치합니다.
echo "Installing pip ..."
sudo curl https://bootstrap.pypa.io/get-pip.py -o $SSPJ_HOME/utilities/tmp/get-pip.py
echo "Running get-pip.py ..."
sudo python $SSPJ_HOME/utilities/tmp/get-pip.py

# AWS CLI를 설치합니다.
echo "Instailling awscli ..."
sudo pip install --ignore-installed awscli

# AWS ElasticBeanstalk CLI를 설치합니다.
echo "Instailling awsebcli ..."
sudo pip install --ignore-installed awsebcli

# AWS Credential을 만듭니다.
echo "Input AWS Access Key : "
read AWS_ACCESS_KEY
echo "Input AWS Secret Access Key : "
read AWS_SECRET_ACCESS_KEY

sudo mkdir ~/.aws
sudo chmod -R 777 ~/.aws
sudo touch ~/.aws/credentials
sudo cat > ~/.aws/credentials << EOF
[default]
aws_access_key=$AWS_ACCESS_KEY
aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
EOF
sudo touch ~/.aws/config
sudo cat > ~/.aws/config << EOF
[profile eb-cli]
aws_access_key_id=$AWS_ACCESS_KEY
aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
EOF

# PATH를 터미널에 적용하기 위해 source를 해줍니다.
source ~/.bash_profile

# 끝!
echo "Done!"
