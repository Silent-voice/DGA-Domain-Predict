# DGA-Domain-Predict
使用LSTM模型检测DGA域名


一、 数据格式

    (一) 二分类

        (1) 训练数据
            1. 一行一组数据
            2. 格式：域名 类型
            3. 0代表非DGA域名，1代表DGA域名

            eg:
                y71f2169b8572150ffd4ac497a5f38c801.hk 1
                timoneuwtihe.ddns.net 1
                l2c89945113a3984626c14d00778abb7d7.cn 1
                taojindi.com 0
                ggmee.com 0


        (2) 测试数据
            1. 同训练数据，不过没有类型

            eg:
                cobjjozfxzadnvzvn.net
                ezqpqtude.com
                jveugx.com
                edujgzyd.org
                abhhlyftdpxa.dyn


        (3) 返回结果
            1. 一行一个结果，对应测试数据，结果是float类型，对应着相应域名是DGA生成的概率

            eg:
                [0.6172037720680237]
                [0.9998446702957153]
                [0.9998708963394165]
                [0.5719057321548462]




    (二) 多分类

        (1) 训练数据
            1. 一行一组数据
            2. 格式：域名 类型

            eg:
                beovglu.info 65
                axdikdjkpnkwv8.com 78
                aabvenhancedysb.com 67
                fhymxxqkyndlpqp.co.uk 50
                chinapyg.com 0



        (2) 测试数据
            1. 同训练数据，不过没有类型

            eg:
                emsesgumwwbvtcbh.eu
                transrush.com
                bbrcqtndpjlt.com
                monyer.com
                vatoefurex.ddns.net


        (3) 返回结果
            1. 一行一个结果，对应测试数据，结果是相应域名的类型

            eg:
                77
                24
                0
                3
                0


二、 程序使用

    (一) 二分类训练
        命令行：python main.py 0 dataFilePath modelFilePath

        参数说明：
            dataFilePath : 训练数据文件路径
            modelFilePath : 训练好的模型文件保存路径，是个文件路径


    (二) 二分类测试
        命令行：python main.py 1 dataFilePath modelFilePath resultFilePath

        参数说明：
            dataFilePath : 测试数据文件路径
            modelFilePath : 加载模型路径
            resultFilePath : 判别结果保存路径，是个文件路径


    (三) 多分类训练
        命令行：python main.py 2 dataFilePath modelFilePath nb_classes

        参数说明：
            dataFilePath : 训练数据文件路径
            modelFilePath : 训练好的模型文件保存路径，是个文件路径
            nb_classes : 训练数据中数据的类型个数，比如：正常域名 + 5种DGA feed生成的域名  nb_classes = 6


    (四) 多分类测试
        命令行：python main.py 3 dataFilePath modelFilePath resultFilePath

        参数说明：
            dataFilePath : 测试数据文件路径
            modelFilePath : 加载模型路径
            resultFilePath : 判别结果保存路径，是个文件路径

