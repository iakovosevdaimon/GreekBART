import argparse
import random
import os


def split_dataset():
    parser = argparse.ArgumentParser()

    parser.add_argument('--path', '-p', default=None, type=str, help='Path to input text file')
    parser.add_argument('--train_split', '-tr', default=0.7, type=float, help='Percentage of training set(i.e. if you want 70% of corpus to be the train set, define this parameter as 0.7)')
    parser.add_argument('--valid_split', '-val', default=0.3, type=float, help='Percentage of validation set')
    parser.add_argument('--test_split', '-ts', default=0.0, type=float, help='Percentage of test set')
    parser.add_argument('--num', '-n', default=None, type=int, help='Number of sentences of input file')
    parser.add_argument('--to', '-t', default=None, type=str, help='Directory to save output')
    parser.add_argument('--test_set', '-test', action='store_true', help='Set this parameter if you want a test set. Default value is False')
    parser.add_argument('--seed', '-s', default=7, type=int)

    args = parser.parse_args()
    random.seed(args.seed)
    train_file = args.to + 'train.el'
    valid_file = args.to + 'valid.el'
    test_file = args.to + 'test.el'
    have_test = args.test_set
    if not os.path.exists(args.to):
        os.system("mkdir -p " + args.to)
    if args.num is None:
        with open(args.path, 'rt', encoding='utf-8') as f:
            c = 0
            for line in f:
                c += 1
    else:
        c = args.num
    fw_tr = open(train_file, 'w', encoding='utf-8')
    fw_val = open(valid_file, 'w', encoding='utf-8')
    if have_test:
        fw_ts = open(test_file, 'w', encoding='utf-8')
    train_lines = int(args.train_split * c)
    if have_test:
        valid_lines = int(args.valid_split * c)
        test_lines = c - (train_lines + valid_lines)
        test_indices = random.sample(range(c), test_lines)
        options = [i for i in range(c)] - test_indices
        valid_indices = set(random.sample(options, valid_lines))
        test_indices = set(test_indices)
        assert len(test_indices) == test_lines, "Mismatch in test's lines indices"
    else:
        valid_lines = c - train_lines
        valid_indices = set(random.sample(range(c), valid_lines))

    assert len(valid_indices) == valid_lines, "Mismatch in validation's lines indices"

    count_train = 0
    count_valid = 0
    count_test = 0
    with open(args.path, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if have_test:
                if i in test_indices:
                    if count_test == test_lines - 1:
                        if line.endswith('\n'):
                            line = line.replace('\n', '')
                        fw_ts.write(line)
                    else:
                        if line.endswith('\n'):
                            fw_ts.write(line)
                        else:
                            fw_ts.write(line + '\n')
                    count_test += 1
                elif i in valid_indices:
                    if count_valid == valid_lines - 1:
                        if line.endswith('\n'):
                            line = line.replace('\n', '')
                        fw_val.write(line)
                    else:
                        if line.endswith('\n'):
                            fw_val.write(line)
                        else:
                            fw_val.write(line + '\n')
                    count_valid += 1
                else:
                    if count_train == train_lines - 1:
                        if line.endswith('\n'):
                            line = line.replace('\n', '')
                        fw_tr.write(line)
                    else:
                        if line.endswith('\n'):
                            fw_tr.write(line)
                        else:
                            fw_tr.write(line + '\n')
                    count_train += 1
            else:
                if i in valid_indices:
                    if count_valid == valid_lines - 1:
                        if line.endswith('\n'):
                            line = line.replace('\n', '')
                        fw_val.write(line)
                    else:
                        if line.endswith('\n'):
                            fw_val.write(line)
                        else:
                            fw_val.write(line + '\n')
                    count_valid += 1
                else:
                    if count_train == train_lines - 1:
                        if line.endswith('\n'):
                            line = line.replace('\n', '')
                        fw_tr.write(line)
                    else:
                        if line.endswith('\n'):
                            fw_tr.write(line)
                        else:
                            fw_tr.write(line + '\n')
                    count_train += 1
    fw_tr.close()
    fw_val.close()
    if have_test:
        fw_ts.close()
    # print train_lines


if __name__ == "__main__":
    split_dataset()