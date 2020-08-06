# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import numpy as np  # numpy数据处理库
from wordcloud import WordCloud, ImageColorGenerator # 词云展示库
from PIL import Image  # 图像处理库
import matplotlib.pyplot as plt  # 图像展示库

# 主函数
def generate_cloud(li):
    path_stopwd = './metadata/stopword.txt'
    path_imag = './metadata/img/wd_background.png'
    for each in li:
        path_txt = f'./metadata/execed_txt/{each}_execed.txt'
        path_store = f'./metadata/img/{each}_wd.png'
        mask = np.array(Image.open(path_imag))
        with open(path_txt, 'r+', encoding='utf-8') as f:
            cut_text = f.read()
        word_cloud = WordCloud(#width = 800,
                            #height= 1600,
                            scale=2,
                            colormap='tab20',  # 设置matplotlib的颜色映射
                            contour_color='grey',
                            background_color='white',  # 设置mode为RGBA且设置background_color为None,将
                            font_path='./metadata/华文圆体 REGULAR.TTF',  # 设置字体格式
                            mask=mask,  # 设置背景图
                            max_words=6000,  # 最多显示词数
                            max_font_size=80).generate(cut_text)
        word_cloud.to_file(path_store)
        '''
        image_colors = ImageColorGenerator(mask)
        # 下面代码表示显示图片
        plt.imshow(word_cloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        plt.show()
        '''

if __name__ == '__main__':
    dic_add = '666 fadf jjj'
    run = GenerateCloud(dic_add)  # 模拟传参--测试
