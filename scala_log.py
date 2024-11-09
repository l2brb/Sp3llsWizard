import numpy as np

# Genera una scala logaritmica più granulare tra 10 e 10,000
log_intervals = list(np.logspace(1, 4, num=15, dtype=int))
print(log_intervals)

# [np.int64(10), np.int64(16), np.int64(26), np.int64(43), np.int64(71), np.int64(117), np.int64(193), np.int64(316), np.int64(517), np.int64(848), np.int64(1389), np.int64(2275), np.int64(3727), np.int64(6105), np.int64(10000)]

# [10, 16, 26, 43, 71, 117, 193, 316, 517, 848, 1389, 2275, 3727, 6105, 10000]