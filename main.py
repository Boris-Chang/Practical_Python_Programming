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
