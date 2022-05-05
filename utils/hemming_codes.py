class Hemming:

    def __init__(self, chunk_length=8):
        self.chunk_length = chunk_length  # задаём длину блока кодирования
        self.control_bits = [i for i in range(1, self.chunk_length + 1) if not i & (i - 1)]  # контрольные биты,
        # являются степенями двойки

    def chars_to_bin(self, chars) -> str:
        """
        Преобразование символов в бинарный формат
        """
        assert not len(chars) * 8 % self.chunk_length, 'Длина кодируемых данных должна быть кратна длине блока ' \
                                                       'кодирования '
        return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])

    @staticmethod
    def chunk_iterator(text_bin, chunk_size):
        """
        Генератор блоков бинарных данных
        """
        for i in range(len(text_bin)):
            if not i % chunk_size:
                yield text_bin[i:i + chunk_size]

    def get_control_bits_data(self, value_bin):
        """
        Получение информации о контрольных битах из бинарного блока данных
        """
        check_bits_count_map = {k: 0 for k in self.control_bits}
        for index, value in enumerate(value_bin, 1):
            if int(value):
                bin_char_list = list(bin(index)[2:].zfill(8))
                bin_char_list.reverse()
                for degree in [2 ** int(i) for i, value in enumerate(bin_char_list) if int(value)]:
                    check_bits_count_map[degree] += 1
        check_bits_value_map = {}
        for check_bit, count in check_bits_count_map.items():
            check_bits_value_map[check_bit] = 0 if not count % 2 else 1
        return check_bits_value_map

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
        value_bin = self.set_empty_control_bits(value_bin)
        check_bits_data = self.get_control_bits_data(value_bin)
        for check_bit, bit_value in check_bits_data.items():
            value_bin = '{0}{1}{2}'.format(
                value_bin[:check_bit - 1], bit_value, value_bin[check_bit:])
        return value_bin

    def encode(self, source, is_bin=False) -> str:
        """
        Кодирование данных
        """
        text_bin = source
        if not is_bin:
            text_bin = self.chars_to_bin(source)
        result = ''
        for chunk_bin in self.chunk_iterator(text_bin, self.chunk_length):
            chunk_bin = self.set_control_bits(chunk_bin)
            result += chunk_bin
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

    def check_and_fix_error(self, encoded_chunk):
        """
        Проверка и исправление ошибки в блоке бинарных данных
        """
        # TODO: алгоритм проверки ошибок
        return encoded_chunk

    def decode(self, encoded, fix_errors=True):
        """
        Декодирование данных
        """
        decoded_value = ''
        fixed_encoded_list = []
        # разделение на блоки для декодирования и исправления ошибок
        for encoded_chunk in self.chunk_iterator(encoded, self.chunk_length + len(self.control_bits)):
            if fix_errors:
                encoded_chunk = self.check_and_fix_error(encoded_chunk)
            fixed_encoded_list.append(encoded_chunk)

        # удаление контрольных битов из сообщения
        clean_chunk_list = []
        for encoded_chunk in fixed_encoded_list:
            encoded_chunk = self.exclude_control_bits(encoded_chunk)
            clean_chunk_list.append(encoded_chunk)

        # декодирование бинарных блоков и объединение в одно сообщение
        for clean_chunk in clean_chunk_list:
            for clean_char in [clean_chunk[i:i + 8] for i in range(len(clean_chunk)) if not i % 8]:
                decoded_value += chr(int(clean_char, 2))
        return decoded_value
