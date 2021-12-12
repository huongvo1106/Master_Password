import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import sys
import struct
import RS
import pandas as pd
import time



def encryption(filename):
    #items need for prepare encryption  
    key = "abcdefghji123456abcdefghji123456"
    key = key.encode('utf-8')
    iv = os.urandom(16)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    chunk_size=64*1024
    output_filename = filename + '.encrypted'
    encryptor = cipher.encryptor()
    filesize = os.path.getsize(filename)
    
    with open(filename, 'rb') as inputfile:
        with open(output_filename, 'wb') as outputfile:
            outputfile.write(struct.pack('<Q', filesize))
            outputfile.write(iv)
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += (b'\x00') * (16 - len(chunk) % 16)
                outputfile.write(encryptor.update(chunk))

    return output_filename
            

            

def decryption(filename):
    
    path = 'actualFile'
    os.chdir(path)

    key = "abcdefghji123456abcdefghji123456"
    key = key.encode('utf-8')
    output_filename = filename[0:-10]

    chunk_size=24*1024
    backend = default_backend()
    
    with open(filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        #get iv from the first 16 bits
        iv = infile.read(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        os.chdir("../")
        with open(output_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.update(chunk))
            outfile.truncate(origsize)


def decode(file_name, arr_VM, k):
    import connection
    
    os.chdir('fragments')

    for filename in os.listdir('.'):
        os.remove(filename)

    need_file = 0
    for num in range(0,file_name):
        vm = num % len(arr_VM)
        #print(vm)
        connection.file_download(arr_VM[vm], str(num), str(num))
        '''
        w = connection.file_download(arr_VM[vm], str(num), str(num))
        if w == True:
            need_file += 1

        if need_file == k:
            break
        '''


    os.chdir('../')

def encode(arr_VM):
    os.chdir('fragments')
       
    i = 0
    for filename in os.listdir('.'):
        print(filename)
        import connection
        if i >= len(arr_VM):
            i = 0
            
        connection.file_upload(arr_VM[int(filename) % len(arr_VM)], filename, filename)

        os.remove(filename)
        i = i + 1
     

#IP Address taken
def get_IP():   
    df = pd.read_excel('insert_IP.xlsx')
    arr_ip = df['IP_add']
    return arr_ip

#get in_put
choose_function = sys.argv[1]
file = sys.argv[2]
n = sys.argv[3]
k = sys.argv[4]


n = int(n)
k = int(k)
arr_VM = get_IP()

if (choose_function == "encryption"):
    encrypted_file = encryption(file)
    os.remove(file)
    success = RS.encode_RS(encrypted_file, n, k)
    if success == True:
        print("ec worked")
    else:
        print("ec did not work")
    os.remove(encrypted_file)

    encode(arr_VM)

 
if (choose_function == "decryption"):
    
    decode(int(n), arr_VM, k)
    time.sleep(3)
    success = RS.decode_RS(file, n, k)
    if success == True:
        print("ec worked")
    else:
        print("ec did not work")

    decryption(file) 

    path = 'actualFile'
    os.chdir(path)
    os.remove(file)
    print("Complete")


