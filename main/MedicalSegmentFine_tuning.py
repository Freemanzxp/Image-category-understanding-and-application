"""
Created on ：2018/5/21
@author: Freeman
"""
from keras.callbacks import Callback
from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.layers import Dense
from keras.optimizers import SGD
import matplotlib.pyplot as plt


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch':[], 'epoch':[]}
        self.accuracy = {'batch':[], 'epoch':[]}
        self.val_loss = {'batch':[], 'epoch':[]}
        self.val_acc = {'batch':[], 'epoch':[]}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        # plt.savefig("loss-acc/epochs_10.png")
        plt.show()


# build the VGG16 network
def vgg16_model(img_rows, img_cols, num_classes=5):
    model = VGG16(weights='imagenet', include_top=True)
    # for i in model.layers:
    #     print(i.name)
    #     print(i.get_weights())
    # print(model.get_layer('block4_conv3').get_weights())
    # model.summary()
    model.layers.pop()
    model.layers.pop()
    model.layers.pop()
    model.outputs = [model.layers[-1].output]
    x=Dense(1024, activation='relu')(model.layers[-1].output)
    x=Dense(128, activation='relu')(x)
    x=Dense(num_classes, activation='softmax')(x)
    model=Model(model.input,x)
    for layer in model.layers[:15]:
        layer.trainable = False
    sgd = SGD(lr=1e-3, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    return model


def train_save_model():
    # 图片生成器:用以生成一个batch的图像数据，
    # 支持实时数据提升。训练时该函数会无限生成数据，直到达到规定的epoch次数为止。
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical')

    # fine-tune the model
    model = vgg16_model(224, 224, 3)

    # loss-history
    history = LossHistory()
    model.fit_generator(
        train_generator,
        steps_per_epoch=16,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=16,
        callbacks=[history]
    )

    loss, acc = model.evaluate_generator(
        validation_generator,
        steps=8)

    print("loss:", loss, "acc:", acc)
    history.loss_plot('epoch')
    # 保存model
    # model.save('MedicalSegmentClassificationModel_weights_10.h5')


if __name__ == "__main__":
    # 参数初始化
    img_width, img_height = 224, 224
    train_data_dir = '../dataSegment/train'
    validation_data_dir = '../dataSegment/validation'
    epochs = 15
    batch_size = 16  # 每次训练样本数

    # 训练模型
    train_save_model()