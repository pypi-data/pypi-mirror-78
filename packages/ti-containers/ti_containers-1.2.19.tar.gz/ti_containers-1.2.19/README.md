# TI Containers

## 了解 TI Containers
1. TI Containers 是腾讯云智能钛机器学习平台 TI-ONE 提供的 TI SDK 训练任务的容器环境初始化工具。
2. TI Containers 支持基于Tensorflow、Pytorch、MXNet、Scikit-Learn框架，以及Horovod的提交的训练任务初始化准备工作。
3. 用户可基于 TI Containers，构建符合自身应用的训练镜像。

## 安装 TI Containers
### 环境要求
Python2.7、Python3.6及以上

### 源码安装
```
python setup.py install
```

### 生成whl包
```
python setup.py bdist_wheel
```

## TI Containers 训练规范
### 目录规范
用户在通过TI SDK提交训练任务后，TI训练后台将会初始化训练任务的容器环境，主要包括：
1. 拉取训练的多个通道数据到输入数据目录/opt/ml/input/data/，以通道名称进行目录布局
2. 构建训练实例需要的超级参数配置、资源配置、通道配置到输入配置目录/opt/ml/input/config/
3. 若用户提供训练entry point，拉取训练代码到代码目录/opt/ml/code

例如，某个训练任务，TI SDK构建的目录结构形式如下：
```
|-- code
|   `-- train.py
|-- input
│　　`── config
│　　    ├── hyperparameters.json
│　　    └── resourceconfig.json
│　　    └── inputdataconfig.json
|   `-- data
|       `-- train
|           `-- train.tfrecords
|       `-- test
|           `-- test.tfrecords
|-- model
`-- output
    `-- failure
```

具体的目录含义为：

| 名称  | 路径   | 备注  |
| --- | --- | --- |
| 代码目录     | /opt/ml/code/  | 存放训练代码的目录  
| 输入目录     | /opt/ml/input/  | 存放训练输入相关的目录  
| 输入配置目录 | /opt/ml/input/config/  | 存放训练相关的配置文件  
| 超级参数文件 | /opt/ml/input/config/hyperparameters.json | 训练任务的超参数列表，json格式，读取值是为string格式   
| 资源配置文件 | /opt/ml/input/config/resourceconfig.json  | 训练任务的资源信息，json格式，主要包括current_host和hosts   
| 通道配置文件 | /opt/ml/input/config/inputdataconfig.json  | 训练任务的输入数据源信息，json格式，读取值主要是通道名称  
| 输入数据目录 | /opt/ml/input/data/  | 存放训练数据的目录，以通道名称为进行目录布局  
| 模型目录     | /opt/ml/model/ | 模型文件将被自动压缩为tar包格式上传到COS 
| 输出目录     | /opt/ml/output/  | 存放训练过程的日志文件，训练失败时将把FailReason写进failure文件


其中/opt/ml/input/config/resourceconfig.json的具体示例如下：
```
{"current_host":"timaker-test-worker-0.worker.timaker-test.svc.cluster.local","hosts":["timaker-test-worker-0.worker.timaker-test.svc.cluster.local"]}
```

/opt/ml/input/config/hyperparameters.json的具体示例如下：
```
{"ti_enable_gpu_exclusive":"true","batch-size":"128","ti_enable_cls_log":"true"}
```

/opt/ml/input/config/inputdataconfig.json的具体示例如下：
```
{"training":{"TrainingInputMode":"File"}}
```


### 环境变量
TI Containers 提供了训练环境各种资源和参数环境变量定义，在训练脚本中可以直接访问这些环境变量获取相关属性，包括：

| 名称  | 含义 |
| --- | --- |
TM_NUM_GPUS | 表示训练实例可用的GPU数目
TM_NUM_CPUS | 表示训练实例可用的CPU数目
TM_HPS |  表示训练任务指定的超参数列表，json表示；例如{"train-steps": 500, "batch-size": 128}
TM_CURRENT_HOST | 表示训练任务的Host名称，例如algo-host-0
TM_HOSTS | 表示训练任务的Host列表，json表示；例如["algo-host-0"，"algo-host-1"]
TM_CHANNELS | 表示通道名称列表，默认为["training"]; <br> 若设置train和test两个通道，则对应的环境变量是["train"、"test"]
TM_CHANNEL_XXX | 表示输入训练数据的路径，XXX对应通道的名称，默认为training；<br>若设置train和test两个通道，则对应的环境变量是TM_CHANNEL_TRAIN和TM_CHANNEL_TEST
TM_MODEL_DIR | 表示训练实例中模型的输出路径，值为/opt/ml/model
TM_OUTPUT_DATA_DIR | 表示训练实例中输出数据的路径，值为/opt/ml/output/data，包括failure等文件
TM_INPUT_CONFIG_DIR | 表示训练实例中输入配置的路径，路径下包括hyperparameters.json、resourceconfig.json、inputdataconfig.json
TM_NETWORK_INTERFACE_NAME | 表示训练实例中使用的网卡设备名称，如eth0

### 启动规范
TI SDK 训练任务执行train命令启动训练：
1. TI Containers已支持train命令启动训练，因此所有内置镜像均已支持train命令启动；
2. 如果是自定义镜像任务，你需要构建自己的train命令，并放入系统环境变量中，以便启动训练；自定义镜像任务具体参见 [使用自定义镜像训练模型](https://cloud.tencent.com/document/product/851/40126)
