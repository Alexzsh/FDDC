import os
import pandas as pd



dirname='../FDDC'
def giveHeTongBIO(filename):
    filename=os.path.join(dirname,filename)
    df=pd.read_csv(filename,delimiter='\t')
if __name__ == "__main__":
    df = pd.read_csv(os.path.join(dirname,'hetong.train'), delimiter='\t')
    print(df.head())
