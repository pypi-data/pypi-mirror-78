from licensing.models import *
from licensing.methods import Key, Helpers
from pynvn.crypt import write_key,load_key,encrypt,decrypt
from pynvn.mc_id import mcwd_id
import tkinter as tk
def authkey(auth = "WyI0MzQ5NyIsIm8rRGJXcjBJNUo3aWYwUk5URUJNaXdZZWdHSlZZbmwxMHFoK2JEQ0ciXQ==",
            product_id = None,
            rsa_pub_key = "<RSAKeyValue><Modulus>n5Q5BtZIlprf+d74p2YmQT1ZnRrCFGqt9JtAzO29/eNbzaM9rFZ5IaD8iIqbc0gVrE2ZFA0tfCtzeAVdV6MlaDaaqexNIZARMBK4dk9AEZb9kAOzdUXZNLv6O3+HyZg6bV75Gj6xFY17YUCefDol5Fyn0Z072lFXUV1DArgb+i2r/YDBI/QTS0crHMUS7iXdlWRk1DdGABvrvtoR78P6+uci5njxjlkniByBODyRMAoml1zk9YBRrCEXi6HLxlurd2Y29QizHRTCACCZP3WsNSiyKZqgKOOjUnZyi+hMX8+W06tcofsjjbKa7D+csFQi0MeL5juiNM3om0vtSD6zjQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>",
            key = None,
            pathtokey = None,
            pathtovaluecsv_key = None,
            using_permanent_key = False,
            valueser_key = "",
            path_mc_id = "",
            ser_key = ""
            ):
    """ auth key """
    result = Key.activate(token=auth,\
                   rsa_pub_key=rsa_pub_key,\
                   product_id=product_id, \
                   key=key,\
                   machine_code=Helpers.GetMachineCode()
                   )
    if (result[0] == None or not Helpers.IsOnRightMachine(result[0])) and using_permanent_key ==  False:
        # an error occurred or the key is invalid or it cannot be activated
        # (eg. the limit of activated devices was achieved)
        # in this case not connect server 
        if "11001" in  result[1] :
            return _active_or_not(pathtokey =pathtokey,
                                            pathtovaluecsv_key = pathtovaluecsv_key 
                                            )
        # case for not actived 
        else:
            write_key(path=pathtokey)
            key = load_key(pathtokey)
            encrypt(filename=pathtovaluecsv_key,
                    key = key,
                    nametow=b"Not actived")
            return [False]

    elif using_permanent_key:
        return  __check_permanent_key(path_mc_id = path_mc_id,
                                        valueser_key=valueser_key,
                                        pathtokey=pathtokey,
                                        ker_ser=key,
                                        ser_key = ser_key
                                        )
            
    else:
        # everything went fine if we are here!
        write_key(path=pathtokey)
        key = load_key(pathtokey)
        encrypt(filename=pathtovaluecsv_key,
                key = key,
                nametow=b"actived")
        license_key = result[0]
        return [True,str(license_key.expires)]
def _active_or_not(pathtokey,pathtovaluecsv_key):
    """ check if it can not connect to server """
    key = load_key(pathtokey)
    k = decrypt(filename=pathtovaluecsv_key,
                key = key
                )
    if k == "actived":
        return [True]
    else:
        return [False]
def __check_permanent_key(path_mc_id,
                            valueser_key,
                            pathtokey,
                            ker_ser,
                            ser_key
                            ):
    key = load_key(ser_key)
    try:
        key_value_de =  decrypt(filename=valueser_key,
                                key = key
                                )
    except:
        key_value_de = ""

    try:
        idmc = decrypt(filename=path_mc_id,
                        key = key
                        )
    except:
        idmc = ""
    if mcwd_id() == idmc  and key_value_de == ker_ser:
        return [True,"The key is used indefinitely"]
    else:
        return [False]