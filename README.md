# GEMS python

Convert matlab code to python code in GEMS project.

## Setting
1. 
```
git clone https://github.com/cogito288/GEMS_python.git
```

2. 
```bash
cd GEMS_python/install
```

3. Modify GEMS_HOME  in install_01_common.sh
```bash
chmod +x install_01_common.sh
source install_01_common.sh
```

4-1. You should modify grib_api_dir in install/pygrib_setup.cfg.template to indicate eccodes build.
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

6. Exceute files

```bash
cd python-refactor/Code/pre_01_raw
python GOCI_01_extract_variables.py
```
