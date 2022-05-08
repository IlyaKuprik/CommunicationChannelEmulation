class Hemming:

    def __init__(self, msg_len=None):
        self.length = 8  # задаём длину одного символа
        self.control_bits = [i for i in range(1, msg_len * self.length + 1) if not i & (i - 1)]  # контрольные биты,
        # являются степенями двойки

    @staticmethod
    def chars_to_bin(chars) -> str:
        """
        Преобразование символов в бинарный формат
        """
        return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])

    def set_empty_control_bits(self, value_bin) -> str:
        """
        Добавить в бинарную строку "пустые" контрольные биты
        На вход: бинарная строка
        На выход: бинарная строка с нулями в позициях контрольных битов
        """
        for bit in self.control_bits:
            value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
        return value_bin

    def get_control_bits_data(self, value_bin) -> str:
        """
        Получение информации о контрольных битах из бинарных данных
        На вход: бинарная строка без контрольных бит
        На выход: строка с уже заполненными контрольными битами
        """

        value_bin = self.set_empty_control_bits(value_bin)
        value_bin = list(value_bin)
        for index in self.control_bits:
            bits_sum = 0
            for i in range(index - 1, len(value_bin), index * 2):
                bits_sum += sum([int(c) for c in value_bin[i:i + index]])
            if bits_sum % 2:
                value_bin[index - 1] = '1'
        return ''.join(value_bin)

    def set_empty_control_bits(self, value_bin) -> str:
        """
        Добавить в бинарный блок "пустые" контрольные биты
        """
        for bit in self.control_bits:
            value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
        return value_bin

    def set_control_bits(self, value_bin) -> str:
        """
        Установить значения контрольных бит
        """

        source_with_bits = self.get_control_bits_data(value_bin)
        return source_with_bits

    def encode(self, source, is_bin=False) -> str:
        """
        Кодирование данных
        На выход: переданное сообщение
        На выход: закодированное сообщение в бинарном формате, с вставленными контрольными битами
        """
        text_bin = source
        if not is_bin:
            text_bin = self.chars_to_bin(source)
        result = self.set_control_bits(text_bin)
        return result

    def exclude_control_bits(self, value_bin) -> str:
        """
        Исключение контрольных битов из value_bin
        На вход: строка с контрольными битами
        На выход: строка, меньшего размера, с исключенными контрольными битами
        """
        clean_value_bin = ''
        for index, char_bin in enumerate(list(value_bin), 1):
            if index not in self.control_bits:
                clean_value_bin += char_bin

        return clean_value_bin

    def check_and_fix_error(self, encoded_source) -> str:
        """
        Проверка и исправление ошибки в бинарной строке
        На вход: кодированная строка с шумом
        На выход: строка с исправленной ошибкой(одной)
        """
        # удаляем контрольные биты в зашумленной строке
        encoded_without_bits = self.exclude_control_bits(encoded_source)
        # пересчитываем контрольные биты
        new_encoded_source = self.get_control_bits_data(encoded_without_bits)

        # определяем номер бита, в котором ошибка, сложив значения контрольных битов, которые изменились
        err_bit = 0
        for index in self.control_bits:
            if new_encoded_source[index - 1] != encoded_source[index - 1]:
                err_bit += index
        err_bit -= 1

        # если нашлась ошибка, инверируем бит с индексов err_bir
        if err_bit != -1:
            encoded_source = encoded_source[:err_bit] + str(int(not int(encoded_source[err_bit]))) + encoded_source[
                                                                                                     err_bit + 1:]
        return encoded_source

    def decode(self, encoded, to_fix=True) -> str:
        """
        Декодирование данных
        На выход: кодированная строка с шумом
        На выход: декодированная строка. Если to_fix = False, то исправление ошибок проводиться не будет.
        """
        decoded_value = ''

        # исправление ошибок
        if to_fix:
            encoded = self.check_and_fix_error(encoded)

        # удаление контрольных битов из сообщения
        encoded = self.exclude_control_bits(encoded)

        # декодирование бинарных блоков и объединение в одно сообщение
        for clean_char in [encoded[i:i + 8] for i in range(len(encoded)) if not i % 8]:
            decoded_value += chr(int(clean_char, 2))
        return decoded_value
