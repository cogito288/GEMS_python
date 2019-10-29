# GEMS python

Convert matlab code to python code in GEMS project.

## Setting
1. 
```
$ git clone https://github.com/cogito288/GEMS_python.git
```

2. 
```bash
cd GEMS_python/install
```

3. Modify GEMS_HOME 
```bash
chmod +x install_01_common.sh
source install_01_common.sh
```

4. 
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
