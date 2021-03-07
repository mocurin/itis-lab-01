"""Common data generator package"""
from typing import Generator, Sequence
from itertools import cycle, product


# Type hinting
RawDataGenerator = Generator[[Sequence[float], float], None, None]


class DataGenerator:
    def __init__(self, generator: RawDataGenerator, epoch_size: int, stop_epoch: int):
        self._generator = generator
        self._epoch_size = epoch_size
        self._stop_epoch = stop_epoch

    @property
    def epoch(self):
        return zip(range(self._epoch_size), self._generator)

    @property
    def eternity(self):
        return zip(range(self._stop_epoch), self.epoch)

    @property
    def epoch_size(self):
        return self._epoch_size


def boolean_generator(boolean: Sequence[str]) -> RawDataGenerator:
    # Check whether `len(boolean)` is a power of two
    if not (size := len(boolean)) or (size & (size - 1)):
        raise ValueError(f"Given sequence ({boolean}) length does not equal power of two: {size}")

    # Repeat values from (0, 1) `len(boolean)` times in vectors of `log2(len(boolean))` elements
    rows = product((0, 1), repeat=len(boolean).bit_length() - 1)

    # Return indefinite generator of pairs
    return cycle(zip(rows, boolean))


def subset(generator: Generator, mask: Sequence) -> Generator:
    # Allow generator values on non-zero positions from mask
    return (values
            for values, allow
            in zip(generator, mask)
            if allow)