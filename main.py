import subprocess
import pandas as pd
from tqdm import tqdm
from math import ceil
import os
import time

df = pd.read_csv("permutations.csv")
nb_line = df.shape[0]
gap = 500000
end = 0

print("Checking the permutations")
time.sleep(0.5)
for i in tqdm(range(ceil(nb_line/gap))):
    begin = end
    end = min(end+gap, nb_line)
    #creating the subfile of permutations
    df1 = df.iloc[begin:end,:]
    df1.to_csv(os.getcwd()+f"\\input\\permutations{i}.csv", index = False)
    file_output = os.getcwd()+f"\\output\\permutations{i}.csv"
    #checking the permutations in this file
    if not os.path.isfile(file_output):
        args = ["python", os.getcwd()+"\\dnstwist.py", "--registered", "--no_twist", os.getcwd()+f"\\input\\permutations{i}.csv", "--format", "csv", "--output", file_output, "exemple.com"]
        process = subprocess.Popen(args, shell = True)
        process.wait()
    else :
        raise Exception(f"The file {file_output} already exists, please move or remove it.")

print("Concatenation of the files of permutations")
time.sleep(0.5)
df_final = pd.DataFrame()
for j in tqdm(range(ceil(nb_line/gap))):
    if os.stat(os.getcwd()+f"\\output\\permutations{j}.csv").st_size != 0 :
        df_temp = pd.read_csv(os.getcwd()+f"\\output\\permutations{j}.csv")
        df_final = pd.concat([df_final, df_temp], ignore_index=True)

if not df_final.empty:
    df_final.to_csv(os.getcwd()+"\\output\\final_permutations.csv", index = False)