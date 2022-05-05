from utils.hemming_codes import Hemming


source = "D="

coder = Hemming(len(source))
encoded_source = coder.encode(source)
print(f"Строка, поданая на вход: {source}")
print(f"Полученный код: {encoded_source}")
# сделаем ошибку
ind = 6
encoded_source = encoded_source[:ind] + str(int(not int(encoded_source[ind]))) + encoded_source[ind+1:]
print(f"Декодированный код: {coder.decode(encoded_source)}")

# print(chr(int('01000100', 2)), chr(int('00111101', 2)))


