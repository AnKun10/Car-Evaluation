file_path = r"D:\fpt47\Downloads\miss_describe.txt"
miss_describe_row_index = []
with open(file_path, "r") as f:
    line = f.readline()
    while line:
        row_index = int(line.strip())
        miss_describe_row_index.append(row_index)
        # print(row_index)print(row_index)
        line = f.readline()
# print(miss_describe_row_index)
# print(len(miss_describe_row_index))
