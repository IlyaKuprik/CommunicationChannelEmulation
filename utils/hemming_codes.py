import copy


class Hemming:

    def __init__(self, msg_len=None):
        self.length = 8  # задаём длину одного символа
        self.control_bits = [i for i in range(1, msg_len * self.length + 1) if not i & (i - 1)]  # контрольные биты,
        # являются степенями двойки

    def chars_to_bin(self, chars) -> str:
        """
        Преобразование символов в бинарный формат
        """
        return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])

    @staticmethod
    def chunk_iterator(text_bin, chunk_size):
        """
        Генератор блоков бинарных данных
        """
        for i in range(len(text_bin)):
            if not i % chunk_size:
                yield text_bin[i:i + chunk_size]

    def set_empty_control_bits(self, value_bin):
        """
        Добавить в бинарный блок "пустые" контрольные биты
        """
        for bit in self.control_bits:
            value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
        return value_bin

    def get_control_bits_data(self, value_bin) -> str:
        """
        Получение информации о контрольных битах из бинарных данных
        На входе бинарная строка без контрольных бит
        На выходе строка с уже заполненными битами
        """

        value_bin = self.set_empty_control_bits(value_bin)
        print(value_bin)
        for index in self.control_bits:
            bits_sum = 0
            for i in range(index - 1, len(value_bin), index + 1):
                bits_sum += sum([int(value_bin[j]) for j in range(i, min(i + index, len(value_bin)))])
            # TODO: предыдущие 2 строчки нихуя не работают. переделать.
            print(index, bits_sum)
            if not (bits_sum % 2):
                value_bin = value_bin[:index] + '1' + value_bin[index + 1:]
        print(value_bin)
        return value_bin

    def set_empty_control_bits(self, value_bin):
        """
        Добавить в бинарный блок "пустые" контрольные биты
        """
        for bit in self.control_bits:
            value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
        return value_bin

    def set_control_bits(self, value_bin):
        """
        Установить значения контрольных бит
        """

        source_with_bits = self.get_control_bits_data(value_bin)
        return source_with_bits

    def encode(self, source, is_bin=False) -> str:
        """
        Кодирование данных
        """
        text_bin = source
        if not is_bin:
            text_bin = self.chars_to_bin(source)
        # print(f"text_bin: {text_bin}")
        result = self.set_control_bits(text_bin)
        return result

    def exclude_control_bits(self, value_bin):
        """
        Исключить информацию о контрольных битах из блока бинарных данных
        """
        clean_value_bin = ''
        for index, char_bin in enumerate(list(value_bin), 1):
            if index not in self.control_bits:
                clean_value_bin += char_bin

        return clean_value_bin

    def check_and_fix_error(self, encoded_source):
        """
        Проверка и исправление ошибки в бинарной строке
        """
        # TODO: алгоритм проверки ошибок
        encoded_without_bits = self.exclude_control_bits(encoded_source)
        new_encoded_source = self.get_control_bits_data(encoded_without_bits)
        err_bit = 0
        for index in self.control_bits:
            if new_encoded_source[index - 1] != encoded_source[index - 1]:
                err_bit += index
        return encoded_source

    def decode(self, encoded):
        """
        Декодирование данных
        """
        decoded_value = ''

        # исправление ошибок
        fixed_encoded = self.check_and_fix_error(encoded)

        # удаление контрольных битов из сообщения
        fixed_encoded = self.exclude_control_bits(fixed_encoded)

        # декодирование бинарных блоков и объединение в одно сообщение
        for clean_char in [fixed_encoded[i:i + 8] for i in range(len(fixed_encoded)) if not i % 8]:
            decoded_value += chr(int(clean_char, 2))
        return decoded_value
