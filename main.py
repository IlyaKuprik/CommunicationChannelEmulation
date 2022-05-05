from utils.hemming_codes import Hemming


source = "German, privet!!"

coder = Hemming(chunk_length=16)
encoded_source = coder.encode(source)
print(f"Строка, поданая на вход: {source}")
print(f"Полученный код:{encoded_source}")
print(f"Декодированный код {coder.decode(encoded_source)}")