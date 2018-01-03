# -*- coding:utf-8 -*-

def Binary(labelFilePath, resFilePath):

    labelFile = open(labelFilePath, 'r')
    resFile = open(resFilePath, 'r')

    label = []
    result = []

    lines = resFile.readlines()
    for line in lines:
        if line.strip('\n').strip('\r').strip(' ') == '':
            continue

        y = float(line.strip('\n').strip('\r').strip(' ').strip('[').strip(']'))
        if y >= 0.5:
            result.append(1)
        else:
            result.append(0)

    lines = labelFile.readlines()
    for line in lines:
        label.append(int(line.strip('\n').strip('\r').strip(' ')))

    TP = 0
    TN = 0
    FN = 0
    FP = 0

    # for i in range(len(label)):
    #
    #     if(label[i] == 1 and result[i] == 1):
    #         TP +=1
    #     if(label[i] ==1 and  result[i] == 0):
    #         FN += 1
    #     if(label[i] == 0 and result[i] ==0):
    #         TN += 1
    #     if(label[i] == 0 and result[i]== 1):
    #         FP += 1
    white_sum = 0
    black_sum = 0
    for i in range(len(label)):

        if(label[i] != 0 and result[i] == 1):
            black_sum += 1
            TP +=1
        if(label[i] != 0 and  result[i] == 0):
            black_sum += 1
            FN += 1
        if(label[i] == 0 and result[i] ==0):
            white_sum += 1
            TN += 1
        if(label[i] == 0 and result[i]== 1):
            white_sum += 1
            FP += 1

    P = (float)(TP)/(TP+FP)
    R = (float)(TP)/(TP+FN)

    score = 100*2*P*R/(P+R)

    print('P: '+str(P))
    print('R: '+str(R))
    print('Score: '+str(score))
    if white_sum != 0:
        print('误报率: ' + str((float)(FP)/white_sum))
    if black_sum != 0:
        print('漏报率: ' + str((float)(FN)/black_sum))


def Multiclass(labelFilePath, resFilePath):
    res_file = open('Multiclass_result.csv', 'w')
    res_file.write('Domain Type, Precison , Recall , F1 ' + '\n')

    labelFile = open(labelFilePath, 'r')
    resFile = open(resFilePath, 'r')

    label = []
    result = []

    lines = resFile.readlines()
    for line in lines:
        result.append(int(line.strip('\n').strip('\r').strip(' ')))

    lines = labelFile.readlines()
    for line in lines:
        label.append(int(line.strip('\n').strip('\r').strip(' ')))


    result_sum = {}

    for i in range(len(label)):
        if label[i] not in result_sum:
            result_sum[label[i]] = [0,0,0,0]    #TP,FP,FN,TN
    for i in range(len(result)):
        if result[i] not in result_sum:
            result_sum[result[i]] = [0,0,0,0]    #TP,FP,FN,TN

    for i in range(len(label)):
        if label[i] == result[i]:
            result_sum[label[i]][0] += 1
        else:
            result_sum[label[i]][2] += 1
            result_sum[result[i]][1] += 1

    for i in range(len(result_sum.keys())):
        TP = result_sum[i][0]
        FP = result_sum[i][1]
        FN = result_sum[i][2]
        TN = result_sum[i][3]

        if (TP + FP) == 0:
            P = 1
        else:
            P = float(TP) / (TP + FP)

        if (TP + FN) == 0:
            R = 1
        else:
            R = float(TP) / (TP + FN)

        if (P + R) == 0:
            F1 = 1
        else:
            F1 = float(2 * P * R) / (P + R)

        result_sum[i].append(P)
        result_sum[i].append(R)
        result_sum[i].append(F1)
        res_file.write(str(i) + ',' + str(round(P,4)) + ',' + str(round(R,4)) + ',' + str(round(F1,4)) + '\n')

    sum_F1 = 0.0
    sum_P = 0.0
    sum_R = 0.0

    sum_TP = 0.0
    sum_FP = 0.0
    sum_FN = 0.0
    sum_TN = 0.0

    for id in result_sum.keys():
        sum_F1 += float(result_sum[id][6])
        sum_P += float(result_sum[id][4])
        sum_R += float(result_sum[id][5])

        sum_TP += float(result_sum[id][0])
        sum_FP += float(result_sum[id][1])
        sum_FN += float(result_sum[id][2])
        sum_TN += float(result_sum[id][3])


    Micro_P = float(sum_TP) / (sum_TP + sum_FP)
    Micro_R = float(sum_TP) / (sum_TP + sum_FN)
    Micro_F = float(2 * Micro_P * Micro_R) / (Micro_P + Micro_R)
    res_file.write('Micro average,' + str(Micro_P) + ',' + str(Micro_R) + ',' + str(Micro_F) + '\n')

    Macro_P = float(sum_P) / len(result_sum.keys())
    Macro_R = float(sum_R) / len(result_sum.keys())
    Macro_F = float(2 * Macro_P * Macro_R) / (Macro_P + Macro_R)
    res_file.write('Macro average,' + str(Macro_P) + ',' + str(Macro_R) + ',' + str(Macro_F) + '\n')



def Binary_new(classesFilePath, resFilePath):
    leave_out_classes = ['bedep', 'beebone', 'corebot', 'cryptowall', 'dircrypt', 'fobber', 'hesperbot', 'matsnu',
                         'symmi', 'tempedreve']

    res_file = open('Binary_result.csv', 'w')
    res_file.write('Domain Type, Precison , Recall , F1, domains num' + '\n')

    #每个元素是一个数组 [TP, FP, FN, TN]
    feed_id = {}
    feed_num = {}
    feed_count = {}
    feed_id['Alexa'] = 0
    feed_num['Alexa'] = 1000000
    feed_count[0] = [0,0,0,0]

    feedFile = open('./data/black/feeds.txt', 'r')
    lines = feedFile.readlines()
    i = 1
    for line in lines:
        feed_id[line.split(' ')[0]] = i
        feed_num[line.split(' ')[0]] = int(line.strip('\n').strip('\r').split(' ')[1])
        feed_count[i] = [0, 0, 0, 0]
        i += 1
    feedFile.close()

    print (str(len(feed_id.keys())))

    classesFile = open(classesFilePath, 'r')
    resFile = open(resFilePath, 'r')

    classes = []
    result = []

    lines = resFile.readlines()
    for line in lines:
        y = float(line.strip('\n').strip('\r').strip(' ').strip('[').strip(']'))
        if y >= 0.5:
            result.append(1)
        else:
            result.append(0)

    lines = classesFile.readlines()
    for line in lines:
        classes.append(int(line.strip('\n').strip('\r').strip(' ')))

    for i in range(len(result)):
        if result[i] == 1:
            if classes[i] != 0:
                feed_count[classes[i]][0] += 1
            else:
                feed_count[classes[i]][2] += 1

        else:
            if classes[i] != 0:
                feed_count[classes[i]][2] += 1
                feed_count[result[i]][1] += 1
            else:
                feed_count[classes[i]][0] += 1

    for feed in feed_id.keys():
        if feed not in leave_out_classes:
        # if feed in leave_out_classes:
            id = feed_id[feed]
            TP = feed_count[id][0]
            FP = feed_count[id][1]
            FN = feed_count[id][2]
            TN = feed_count[id][3]

            if (TP + FP) == 0:
                P = 1
            else:
                P = float(TP) / (TP + FP)

            if (TP + FN) == 0:
                R = 1
            else:
                R = float(TP) / (TP + FN)

            if (P + R) == 0:
                F1 = 1
            else:
                F1 = float(2 * P * R) / (P + R)

            feed_count[id].append(P)
            feed_count[id].append(R)
            feed_count[id].append(F1)
            res_file.write(feed + ',' + str(P) + ',' + str(R) + ',' + str(F1) + ',' + str(feed_num[feed]) + '\n')


    sum_F1 = 0.0
    sum_P = 0.0
    sum_R = 0.0


    sum_TP = 0.0
    sum_FP = 0.0
    sum_FN = 0.0
    sum_TN = 0.0

    i = 0
    for feed in feed_id.keys():
        if feed not in leave_out_classes:
        # if feed in leave_out_classes:
            i += 1
            id = feed_id[feed]
            sum_F1 += float(feed_count[id][6])
            sum_P += float(feed_count[id][4])
            sum_R += float(feed_count[id][5])


            sum_TP += float(feed_count[id][0])
            sum_FP += float(feed_count[id][1])
            sum_FN += float(feed_count[id][2])
            sum_TN += float(feed_count[id][3])

    print (i)

    Micro_P = float(sum_TP) / (sum_TP + sum_FP)
    Micro_R = float(sum_TP) / (sum_TP + sum_FN)
    Micro_F = float(2 * Micro_P * Micro_R) / (Micro_P + Micro_R)
    res_file.write('Micro,' + str(Micro_P) + ',' + str(Micro_R) + ',' + str(Micro_F) + '\n')

    Macro_P = float(sum_P) / i
    Macro_R = float(sum_R) / i
    Macro_F = float(2 * Macro_P * Macro_R) / (Macro_P + Macro_R)
    res_file.write('Macro,' + str(Macro_P) + ',' + str(Macro_R) + ',' + str(Macro_F) + '\n')


def Binary_normal(classesFilePath, resFilePath):
    leave_out_classes = ['bedep', 'beebone', 'corebot', 'cryptowall', 'dircrypt', 'fobber', 'hesperbot', 'matsnu',
                         'symmi', 'tempedreve']

    res_file = open('Binary_result.csv', 'w')
    res_file.write('Domain Type, right_num , wrong_num , P , support' + '\n')

    #每个元素是一个数组 [right,wrong]
    feed_id = {}
    feed_count = {}
    feed_id['Alexa'] = 0
    feed_count[0] = [0,0]

    feedFile = open('./data/black/feeds.txt', 'r')
    lines = feedFile.readlines()
    i = 1
    for line in lines:
        feed = line.split(' ')[0]
        feed_id[feed] = i
        feed_count[i] = [0,0]
        i += 1
    feedFile.close()

    print (str(len(feed_id.keys())))

    classesFile = open(classesFilePath, 'r')
    resFile = open(resFilePath, 'r')

    classes = []
    result = []

    lines = resFile.readlines()
    for line in lines:
        y = float(line.strip('\n').strip('\r').strip(' ').strip('[').strip(']'))
        if y >= 0.5:
            result.append(1)
        else:
            result.append(0)

    lines = classesFile.readlines()
    for line in lines:
        classes.append(int(line.strip('\n').strip('\r').strip(' ')))

    for i in range(len(result)):
        if result[i] == 1:
            if classes[i] != 0:
                feed_count[classes[i]][0] += 1
            else:
                feed_count[classes[i]][1] += 1

        else:
            if classes[i] != 0:
                feed_count[classes[i]][1] += 1
            else:
                feed_count[classes[i]][0] += 1

    P_sum = 0.0
    num = 0
    for feed in feed_id.keys():
        # if feed not in leave_out_classes:
        if feed in leave_out_classes:

            id = feed_id[feed]
            right_num = feed_count[id][0]
            wrong_num = feed_count[id][1]
            P_true = float(right_num)/(right_num + wrong_num)
            P = round(float(right_num)/(right_num + wrong_num), 4)
            num += 1
            P_sum +=  P_true
            res_file.write(feed + ',' + str(right_num) + ',' + str(wrong_num) + ',' + str(P) + ',' + str(right_num + wrong_num) + '\n')

    res_file.write('average' + ',,,' + str(P_sum/num) + '\n')



# Binary('./data/Binary/11.22/train_test_label_11.22.txt', './result/tanh_12.14/train_result_12.14_tanh_100_8_b.txt')
# Binary('./data/Binary/11.22/train_test_label_11.22.txt', './result/12.11/train_result_12.11_relu_120_3_b.txt')

# Binary('./data/Binary/11.22/test_label_11.22.txt', './result/12.9/test_result_12.9_80_b.txt')
# Binary('./data/Binary/11.22/test_label_11.22.txt', './result/12.9/test_result_12.9_80_1_global_attention_b.txt')
# Binary('./data/Binary/11.22/test_label_11.22.txt', './result/12.11/test_result_12.11_relu_130_5_b.txt')
# Binary('./data/Binary/11.22/test_label_11.22.txt', './result/12.11/test_result_12.11_relu_150_5_b.txt')
# Binary('./data/Binary/11.22/test_label_11.22.txt', './result/tanh_12.14/test_result_12.14_tanh_190_8_b.txt')
# Binary('./data/Binary/11.22/test_label_11.22.txt', './result/linear_12.15/test_result_12.15_linear_120_5_b.txt')

# Binary('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/12.9/leave_out_result_12.9_80_b.txt')
# Binary('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/12.9/leave_out_result_12.9_150_1_global_attention_b.txt')
# Binary('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/12.11/leave_out_result_12.11_relu_130_5_b.txt')
# Binary('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/12.11/leave_out_result_12.11_relu_150_5_b.txt')
# Binary('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/tanh_12.14/leave_out_result_12.14_tanh_190_8_b.txt')
# Binary('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/linear_12.15/leave_out_result_12.15_linear_120_5_b.txt')


# Binary_new('./data/Binary/11.22/test_classes_11.22.txt', './result/12.9/test_result_12.9_80_b.txt')
# Binary_new('./data/Binary/11.22/test_classes_11.22.txt', './result/12.11/test_result_12.11_relu_130_5_b.txt')
# Binary_new('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/12.11/leave_out_result_12.11_relu_120_5_b.txt')


# Binary_normal('./data/Binary/11.22/test_classes_11.22.txt', './result/12.9/test_result_12.9_80_b.txt')
# Binary_normal('./data/Binary/11.22/test_classes_11.22.txt', './result/12.11/test_result_12.11_relu_130_5_b.txt')
# Binary_normal('./data/Binary/11.22/test_classes_11.22.txt', './result/12.11/test_result_12.11_relu_150_5_b.txt')
# Binary_normal('./data/Binary/11.22/test_classes_11.22.txt', './result/tanh_12.14/test_result_12.14_tanh_180_8_b.txt')
# Binary_normal('./data/Binary/11.22/test_classes_11.22.txt', './result/linear_12.15/test_result_12.15_linear_120_5_b.txt')

# Binary_normal('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/12.9/leave_out_result_12.9_80_b.txt')
# Binary_normal('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/12.11/leave_out_result_12.11_relu_130_5_b.txt')
# Binary_normal('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/12.11/leave_out_result_12.11_relu_150_5_b.txt')
# Binary_normal('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/tanh_12.14/leave_out_result_12.14_tanh_180_8_b.txt')
Binary_normal('./data/Binary/11.22/leave_out_classes_11.22.txt', './result/linear_12.15/leave_out_result_12.15_linear_120_5_b.txt')

# Multiclass('./data/Multiclass/11.22/test_label_11.22_10000.txt', './result/12.12/test_result_12.12_50_1_m_10000.txt')
# Multiclass('./data/Multiclass/11.22/test_label_11.22_10000.txt', './result/12.13/test_result_12.13_relu_120_20_m.txt')
# Multiclass('./data/Multiclass/11.22/test_label_11.22_10000.txt', './result/tanh_12.13/test_result_12.13_tanh_100_15_m.txt')
# Multiclass('./data/Multiclass/11.22/train_test_label_11.22_10000.txt', './result/tanh_12.13/train_result_12.13_tanh_120_15_m.txt')

# Multiclass('./data/Multiclass/11.22/test_label_11.22_10000.txt', './result/linear_12.14/test_result_12.14_linear_100_15_m.txt')
# Multiclass('./data/Multiclass/11.22/train_test_label_11.22_10000.txt', './result/linear_12.14/train_result_12.14_linear_80_15_m.txt')
