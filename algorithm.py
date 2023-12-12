from itertools import cycle

class MLTAlgorithm:
    def __init__(self):
        pass

    def apply_mlt(self, message: str) -> str:
        signal_levels = cycle([1, 0, -1, 0])
        signal_level = 0
        encoded = list()

        for bit in message:
            signal_level = next(signal_levels) if bit == '1' else signal_level
            encoded.append(signal_level)
        return encoded

    def reverse_mlt(self, encrypted_message):
        previous = 0 if encrypted_message[0] == 0 else 1
        original_message = [previous,]

        for signal_level in encrypted_message:
            bit = 0 if signal_level == previous else 1
            original_message.append(bit) 
            previous = signal_level

        return original_message