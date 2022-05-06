from utils.hemming_codes import Hemming


source = "privet"

coder = Hemming(len(source))
encoded_source = coder.encode(source)
print(f"Строка, поданая на вход: {source}")
print(f"Полученный код: {encoded_source}")
# сделаем ошибку
ind = 16
encoded_source = encoded_source[:ind] + str(int(not int(encoded_source[ind]))) + encoded_source[ind+1:]
print(f"Декодированный код: {coder.decode(encoded_source, to_fix=False)}")
print(f"Декодированный код с исправлением ошибок: {coder.decode(encoded_source)}")


