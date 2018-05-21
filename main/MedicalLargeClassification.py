"""
Created on ：2018/5/21
@author: Freeman
"""
import numpy as np
from tkinter import *
import tkinter.filedialog
from keras import backend as K
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import load_img, img_to_array


def getLargeFileNames():
    filenames = tkinter.filedialog.askopenfilenames()
    if len(filenames) != 0:
        rightCategroy = ""
        string_filename = ""
        count = 0
        for i in range(0, len(filenames)):
            count += 1
            string_filename += str(filenames[i]) + "\n"
            temp = str(filenames[i]).split('/')[-1].split('.')[0]
            if count % 5 == 0:
                rightCategroy += temp + "\n"
            else:
                rightCategroy += temp + " "
        LargePictureNames.set(string_filename)
        lb1.config(text="图片真实类别：\n" + rightCategroy)
    else:
        LargePictureNames.set('')
        lb1.config(text="您没有选择任何图片")


def Large_model_predict():
    if LargePictureNames.get() != '':
        picList = LargePictureNames.get().split('\n')[:-1]
        data = []
        for i in picList:
            img = load_img(i, target_size=(img_width, img_height))
            x = img_to_array(img)
            data.append(x)
        data = np.stack(data,axis=0)
        data = preprocess_input(data)  # 对样本执行-逐样本均值消减-的归一化
        model1 = load_model('MedicalLargeClassificationModel_weights_15.h5')
        result1 = model1.predict(data)
        K.clear_session()

        model2 = load_model('MedicalSegmentClassificationModel_weights_15.h5')
        result2 = model2.predict(data)
        K.clear_session()

        number = result1.shape[0]
        strs = ''
        count = 0
        for i in range(number):
            count += 1
            res1 = np.max(result1[i])
            categroy = categroyDict1[np.where(result1[i] == res1)[0][0]]
            if count % 5 == 0:
                if categroy == '医学':
                    res2 = np.max(result2[i])
                    segment = categroyDict2[np.where(result2[i] == res2)[0][0]]
                    strs += str(categroy) + '-' + str(segment) + "\n"
                else:
                    strs += str(categroy)+ "\n"

            else:
                if categroy == '医学':
                    res2 = np.max(result2[i])
                    segment = categroyDict2[np.where(result2[i] == res2)[0][0]]
                    strs += str(categroy) + '-' + str(segment) + " "
                else:
                    strs += str(categroy) + " "
        lb3.config(text="预测类别：\n" + strs)
    else:
        lb3.config(text="图片选择有误！")


if __name__ == "__main__":

    # 参数初始化
    img_width, img_height = 224, 224

    # 类别字典
    categroyDict1 ={0:'   动物   ',1:'   室内   ',2:'医学',3:'   人物   ',4:'   交通   '}
    categroyDict2 ={0:'胸部',1:'头部',2:'四肢'}

    # GUI
    root = tkinter.Tk()
    root.geometry('700x550+300+50')

    LargePictureNames = StringVar()
    SegmentPictureNames = StringVar()

    root.title('Image recognition system          Copyright © 2018 by Freeman')
    root['bg'] = '#a9ed96'
    root.attributes("-alpha",0.97)


    lb0 = Label(root, text='图像识别系统', width=20, font = 'Helvetica -20 bold',bg='#a9ed96',height=3)
    lb0.grid(row=0, column=0, stick=W, pady=1,)

    lb5 = Label(root, text='注：若为医学类图像暂时仅支持胸部、头部、四肢识别',bg='#a9ed96', fg='red')
    lb5.grid(row=0, column=1, stick=W)

    btn1 = Button(root, text="选择需要预测的图片", width=20, command=getLargeFileNames)
    btn1.grid(row=1, column=0, stick=W, pady=10, padx=50)

    lb1 = Label(root, text='', width=60)
    lb1.grid(row=1, column=1, pady=20)

    btn3 = Button(root, text="预 测", width=20,  bg='SkyBlue',command=Large_model_predict)
    btn3.grid(row=4, column=0, stick=W,  pady=10, padx=50)

    lb3 = Label(root, text='', width=60)
    lb3.grid(row=4, column=1, pady=30)


    root.mainloop()