# 密码表的生成：
# 1.利用ACII码表随机生成（33，127）任意符号
# 2.利用hash（）函数存放密码表
# 3.通过file操作读，写密码表并用于交付

import random

class CryptIt:
    #类的初始化（构造函数）
    def __init__(self):
        self.alphabet_src = [chr(i) for i in range(33,127)]
        self.alphabet_tar = self.alphabet_src.copy()
        self.alphabet_s2t_dict = dict()
        self.alphabet_t2s_dict = dict()
        random.shuffle(self.alphabet_tar)
        for i in range(len(self.alphabet_src)):
            self.alphabet_s2t_dict[self.alphabet_src[i]] = self.alphabet_tar[i]
            self.alphabet_t2s_dict[self.alphabet_tar[i]] = self.alphabet_src[i]
    #convert_char()函数
    def convert_char(self,single_char:str,operation:str)->str:
        '''对单个字符进行加密/解密
        输入参数：
        single_char:要加密/解密的单个字符
        operation：'encrypt'->加密；'decrypt'->解密
        返回结果：加密/解密后的单个字符
        '''
        result = ''
        if ord(single_char) >= 33 and ord(single_char) <= 126:
            if operation == 'encrypt':
                result = self.alphabet_s2t_dict[single_char]
            elif operation == 'decrypt':
                result = self.alphabet_t2s_dict[single_char]
        else:
            result = single_char
        return result
#加密程序
    def encrypt_it(self,src_str:str)->str:
        '''
        用于对字符串进行简单替换加密
        输入参数：
        scr_str:原始文本
        返回结果：加密文本
        '''
        encrypted_str = ''
        for single_char in src_str:
            encrypted_str += self.convert_char(single_char, 'encrypt')
        return encrypted_str
#解密程序
    def decrypt_it(self,tar_str:str)->str:
        '''用于对加密字符串进行简单替换解密
        输入参数：
        encrypt_str:加密文本内容
        返回结构：解密文本
        '''
        decrypt_str = ''
        for single_char in tar_str:
            decrypt_str += self.convert_char(single_char,'decrypt')
        return decrypt_str

    def assert_crypt(self):
       assert(self.decrypt_it(self.encrypt_it('I love you'))=='I love you')
       print('Assertion Ok!')


my_crypt = CryptIt()
print(my_crypt.encrypt_it('AbCdefgH!'))
