# GEMS python

Convert matlab code to python code in GEMS project.

## Testbad
- OS: Ubuntu 18.04.3 LTS
- python: python3.6

## Tips 
- [카카오 PyPI Mirror 저장소로 PIP 설치 속도 높이기](http://www.kwangsiklee.com/2018/05/%EC%B9%B4%EC%B9%B4%EC%98%A4-pypi-mirror-%EC%A0%80%EC%9E%A5%EC%86%8C%EB%A1%9C-pip-%EC%84%A4%EC%B9%98-%EC%86%8D%EB%8F%84-%EB%86%92%EC%9D%B4%EA%B8%B0/)
- [우분투(ubuntu)의 apt 기본 미러(mirror)를 다음 카카오(kakao), 네오위즈(neowiz), harukasan 으로 변경](https://gist.github.com/lesstif/8185f143ba7b8881e767900b1c8e98ad)
```bash
sudo bash ./change-ubuntu-mirror.sh -k
```


## Setting
1. 
```
git clone https://github.com/cogito288/GEMS_python.git
```

2. 
```bash
cd GEMS_python/install
```

3. Modify GEMS_HOME in install_01_common.sh. GEMS_HOME indicates where GEMS_python is located e.g. GEMS_HOME=/home/sehyun/Downloads/GEMS_python
```bash
chmod +x install_01_common.sh
source install_01_common.sh
```

4-1. eccodes will be installed in your HOME/source/eccodes. Unless it needs to be changed, you don't have to care 4-1 and go to 4-2.

You should modify grib_api_dir in install/pygrib_setup.cfg.template to indicate eccodes build.
Generally, if everything is okay in install_02_packages.sh after installing eccodes, it will be installed in your $HOME/source/eccodes.
e.g. grib_api_dir = /home/sehyun/source/eccodes

4-2.
```bash
chmod +x install_02_packages.sh
source install_02_packages.sh
```

5. Virtual environment activate
```bash
cd ..
source ~/.bashrc
source venv/bin/activate
```

6. Install required packages
```bash
pip install -r requirements.txt
```

7. Exceute files. If needed, please change pathes in files.

```bash
cd python-refactor/Code/pre_01_raw
python GOCI_01_extract_variables.py
```
