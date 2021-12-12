import os
import subprocess

#Encodes a file into fragments and stores in /fragments directory
#filename: full path to the target file., ex:/home/penny/Desktop/test.txt
#N: RS input parameter N
#K: RS input parameter K
def encode_RS(filename, N, K):
    if N<K:
        print("encode fail: K must be <= N")
        return False
    command =  "encode " + filename + " " + str(N) + " " + str(K)
    result = subprocess.run(['java', 'Main', command], capture_output=True, text=True)
    if result.stdout.strip() == "SUCCESS":
        return True
    else:
        print(result.stdout)
        return False
    


#Decodes K fragments from /fragments directory into original file and stores in /actualFile directory
#filename: the name in which the file should be stored as in /actualFile directory
#N: RS input parameter N
#K: RS input parameter K
def decode_RS(filename, N, K):
    if N<K:
        print("decode fail: K must be <= N")
        return False
    command =  "decode " + filename + " " + str(N) + " " + str(K)
    result = subprocess.run(['java', 'Main', command], capture_output=True, text=True)
    if result.stdout.strip() == "SUCCESS":
        return True
    else:
        print(result.stdout)
        return False









#import RS.penny

#RS.encode_RS(filena,e. 3, 2)

#test
#filename = 'My_Password.xlsx'
#N = 5
#K = 2
#encode_RS(filename, N, K)
#decode_RS(filename, N, K)

