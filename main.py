# 密码表的生成：
# 1.利用ACII码表随机生成（33，127）任意符号
# 2.利用hash（）函数存放密码表
# 3.通过file操作读，写密码表并用于交付

import random
import pickle

alphabet_src = [chr(i) for i in range(33,127)]
alphabet_tar = alphabet_src.copy()
random.shuffle(alphabet_tar)

alphabet_s2t_dict = dict()
alphabet_t2s_dict = dict()
for i in range(len(alphabet_src)):
    alphabet_s2t_dict[alphabet_src[i]] = alphabet_tar[i]
    alphabet_t2s_dict[alphabet_tar[i]] = alphabet_src[i]

pickle.dump
(
 [alphabet_s2t_dict,alphabet_t2s_dict],
 open('key.dat','wb')
    
#convert_char()函数
def convert_char(single_char:str,operation:str)->str:
    '''对单个字符进行加密/解密
    输入参数：
    single_char:要加密/解密的单个字符
    operation：'encrypt'->加密；'decrypt'->解密
    返回结果：加密/解密后的单个字符
    '''
    result = ''
    if ord(single_char) >= 33 and ord(single_char) <= 126:
        if operation == 'encrypt':
            result = alphabet_s2t_dict[single_char]
        elif operation == 'decrypt':
            result = alphabet_t2s_dict[single_char]
    else:
        result = single_char
    return result
#加密程序
def encrypt_it(scr_str:str)->str:
    '''用于对字符串进行简单替换加密
    输入参数：
    scr_str:原始文本
    返回结果：加密文本
    '''
    encrypt_str=''
    for single_char in scr_str:
        encrypt_str += convert_char(single_char,'encrypt')
    return encrypt_str
#解密程序
def decrypt_it(encrypt_str:str)->str:
    '''用于对加密字符串进行简单替换解密
    输入参数：
    encrypt_str:加密文本内容
    返回结构：解密文本
    '''
    decrypt_str=''
    for single_char in encrypt_str:
        decrypt_str += convert_char(single_char,'decrypt')
    return decrypt_str

