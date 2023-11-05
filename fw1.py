import random
import csv
import os

with open("sample.csv", "r", encoding="utf-8") as csv_file:
    data = list(csv.reader(csv_file))


def show(output_type="top", number=5, separator=","):
    if len(data[1:]) >= number:
        flag = True
    else:
        flag = False

    if output_type == "top":
        if flag:
            order = list(range(1, number+1))
        else:
            order = list(range(1, len(data)))
    elif output_type == "bottom":
        if flag:
            order = list(range(-1, -(number+1), -1))
        else:
            order = list(range(-1, -len(data), -1))
    elif output_type == "random":
        if flag:
            order = random.sample(range(1, len(data)), number)
            print(order)
        else:
            order = random.sample(range(1, len(data)), len(data)-1)
            print(order)

    order.insert(0, 0)

    string_max_lengths = []
    for j in range(len(data[0])):
        lengths = []
        for i in order:
            lengths.append(len(data[i][j]) + len(separator))
        string_max_lengths.append(max(lengths))

    for i in order:
        columns_number = len(data[i])
        for j in range(columns_number):
            if j == columns_number - 1:
                print('{:{}}'.format(data[i][j], string_max_lengths[j] - len(separator)), end="")
            else:
                print('{:{}}'.format(data[i][j] + separator, string_max_lengths[j]), end=" ")
        print()
        if i == 0:
            print()
    print()


def info():
    columns = len(data[0])
    rows = len(data[1:])
    print(str(rows)+"x"+str(columns))

    data_info = []

    for j in range(len(data[0])):
        data_info.append([0, ''])
        for row in data[1:]:
            if len(row[j]) != 0:
                data_info[j][0] += 1
                if data_info[j][1] != str(type(row[j])):
                    data_info[j][1] = str(type(row[j])).replace("<class '", "").replace("'>", "")

    max_length = max(len(header) for header in data[0])

    for i in range(len(data[0])):
        print("{:{}}".format(data[0][i], max_length), data_info[i][0], data_info[i][1])
    print()


def del_nan():
    indexes_to_delete = []
    for i in range(len(data)):
        sum_length = 0
        for j in range(len(data[0])):
            sum_length += len(data[i][j])
        if sum_length == 0:
            indexes_to_delete.append(i)
    for index in indexes_to_delete:
        del data[index]


def make_ds():
    number = len(data[1:])
    train_number = round(number * 0.7)
    test_number = number - train_number

    normal_order = list(range(1, len(data)))
    normal_set = set(normal_order)
    train_order = random.sample(normal_order, train_number)
    train_set = set(train_order)
    residual_set = normal_set - train_set
    test_order = random.sample(list(residual_set), test_number)

    learning = "workdata/Learning"
    testing = "workdata/Testing"

    if not os.path.exists("workdata"):
        os.mkdir("workdata")
    if not os.path.exists(learning):
        os.mkdir(learning)
    if not os.path.exists(testing):
        os.mkdir(testing)

    with open(learning+"/train.csv", "w", encoding="utf-8", newline="") as csv_learning:
        writer = csv.writer(csv_learning)
        writer.writerow(data[0])
        for index in train_order:
            writer.writerow(data[index])

    with open(testing+"/test.csv", "w", encoding="utf-8", newline="") as csv_testing:
        writer = csv.writer(csv_testing)
        writer.writerow(data[0])
        for index in test_order:
            writer.writerow(data[index])


show(separator="*")
info()
del_nan()
show("random", 3, ";")
info()
make_ds()
