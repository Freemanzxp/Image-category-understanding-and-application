# 图像的类别理解及应用
- 此库为2017-2018年度工程实践项目，主要目的是能够识别图像类别，尤其是医学类，然后在医学类中再进行更为细致的类别识别，以达到医学影像这一垂直领域的应用目的。

# 环境
- 操作系统：Windows10
- 编程语言：Python3
- 模型框架：Keras
- GPU：GTX 1060
- GUI：Tkinter

# 文件结构及意义
- VGG16_model：存放训练好的VGG16模型——vgg16_weights_tf_dim_ordering_tf_kernels.h5
- main：主文件
  - MedicalLargeClassification.py——图像识别GUI搭建——`运行此文件即可启动程序`
  - MedicalLargeFine_tuning.py——图像大类识别模型搭建
  - MedicalSegmentFine_tuning.py——医学小类识别模型搭建
  - MedicalLargeClassificationModel_weights_15.h5——训练好的图像大类分类模型
  - MedicalSegmentClassificationModel_weights_15.h5——训练好的医学小类分类模型
- picture：
  - craw_picture.py——爬虫系统构建
- testCase：测试样本
- 注：`由于.h5单文件超过了GitHub 100M的限制，项目总大小超过1个G，所以利用LFS进行git push`

# 数据源
- ImageNet开源数据集中的VOC2012一部分，进行类别合并，筛选出人物、动物、室内、交通四大类
- 从国外开源医疗图像网站www.openi.org上爬取图片，进行修剪，最终得到医学类图像
  - 其中医学类又细分为了胸部、头部、四肢三类
- 数据规模：训练集1700张，验证集450张，测试集35张

# 模型
- 模型借鉴了迁移学习的思想，利用基于ImageNet数据集训练好的VGG16模型，释放最后一个卷积核的参数并且pop最后三层，再add三个Dense层。
  - 其实这一步花费了很长时间，因为模型的迁移涉及到两个部分，一个是模型的框架，另一个是模型的参数。
  - 先说官方文档，众所周知，keras的模型结构有两种：Sequential、Model。阅读VGG16的源码可以发现，VGG16是Model结构，而官网文档给的例子是用Sequential结构搭建模型后，将vgg16_weights_tf_dim_ordering_tf_kernels.h5的权重加载进模型，但是实际运行会报错——两种结构并不兼容
  - 再说说博客，几乎所有的blog都和我的想法一致，尝试自己用Model结构搭建模型，但是在Flatten层都会报错，尝试各种写法都报错误
  - 最后我决定不动Flatten层，利用Model的pop()将最后三层Dense删除，再增加合适尺寸的Dense层，问题解决
  - 注：`想要利用训练好的VGG16，最好自己下载，然后改VGG16源码里面的载入地址（因为Keras需要去国外下载，及其慢，本库存放在VGG16_model中）`

# 训练
- 图像大类分类模型训练：人物、动物、室内、交通、医学

  <img src="https://github.com/Freemanzxp/Image-category-understanding-and-application/raw/master/src/4.png" width = "500" />
- 医学小类分类模型训练： 头部。胸部、四肢

  <img src="https://github.com/Freemanzxp/Image-category-understanding-and-application/raw/master/src/5.png" width = "500" />

# GUI
- 利用python的tkinter搭建交互界面
- 将大类识别和医学小类识别串联起来，形成应用。

  <img src="https://github.com/Freemanzxp/Image-category-understanding-and-application/raw/master/src/1.png" width = "500" />


# 测试
- 测试样本：testCase

  <img src="https://github.com/Freemanzxp/Image-category-understanding-and-application/raw/master/src/2.png" width = "500" />
- 测试截图：红线框标注的为分类错误

  <img src="https://github.com/Freemanzxp/Image-category-understanding-and-application/raw/master/src/3.png" width = "500" />
