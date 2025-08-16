class Naturals:
    DEFAULT_START = 1
    DEFAULT_END = 100
    def __init__(self, start_num = DEFAULT_START, end_num = DEFAULT_END):
        self.min_num = start_num
        self.max_num = end_num
        self.list_naturals = list(range(start_num, end_num + 1))

    def extract(self, num_to_extract):
        self.list_naturals.remove(num_to_extract)

    def get_lost(self):
        expected_sum = self.max_num * (self.max_num + 1) / 2
        real_sum = sum(self.list_naturals)

        return expected_sum - real_sum

    def is_valid_to_extract(self, num_to_extract):
        return num_to_extract >= self.min_num and num_to_extract <= self.max_num

    def _get_num_list(self):
        return self.list_naturals