import subprocess

subprocess.call(["python", "GOCI_01_extract_variables.py"])
print ("===========================================================")
subprocess.call(["python", "GOCI_02_generate_missing_nan_file.py"])
#subprocess.call(["python", "GOCI_01_02.py"])
#subprocess.call(["python", "GOCI_01_02.py"])
#subprocess.call(["python", "GOCI_01_02.py"])
#subprocess.Popen("GOCI_03_AOD_filter.py")

