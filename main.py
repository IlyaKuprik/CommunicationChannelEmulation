from utils.hemming_codes import Hemming
from utils.channel import emulate_channel


def emulate(source, P, is_bin=False):
    print(f"Строка, поданая на вход: {source}")
    coder = Hemming(len(source), is_bin=is_bin)
    encoded_source = coder.encode(source)
    print(f"Зкодированная строка, поданая на вход: {encoded_source}")

    result_encoded_source = emulate_channel(P, encoded_source)

    print(f"Закодированная строка c шумом: {result_encoded_source}")
    errs = [k for k, (i, j) in enumerate(zip(list(result_encoded_source), list(encoded_source))) if i != j]
    print("Позиции, в которых возникли ошибки:", errs)
    result_source = coder.decode(result_encoded_source, to_fix=True)
    print(f"Декодированная строка с исправленной ошибкой(одной): {result_source}")


message = "hi"
P_matrix = [[0.9, 0.1], [0.1, 0.9]]
emulate(message, P_matrix, is_bin=False)
