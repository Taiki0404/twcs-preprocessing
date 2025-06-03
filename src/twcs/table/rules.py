class SequenceLength:
    def __init__(self, min: int, max: int):
        if min < 0 or max < 0:
            raise ValueError("Sequence length must be non-negative.")
        if min > max:
            raise ValueError("Minimum length cannot be greater than maximum length.")
        if min == 0 and max == 0:
            raise ValueError("Minimum and maximum length cannot both be zero.")

        self.min = min
        self.max = max
