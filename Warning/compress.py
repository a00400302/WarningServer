from PIL import Image


class Compress_img:

    def __init__(self, img_path):
        self.img_path = img_path
        self.img_name = img_path.split('/')[-1]

    def compress_img_PIL(self, way=1, compress_rate=0.2, show=False):
        '''
        img.resize() 方法可以缩小可以放大
        img.thumbnail() 方法只能缩小
        :param way:
        :param compress_rate:
        :param show:
        :return:
        '''
        img = Image.open(self.img_path)
        w, h = img.size
        # 方法一：使用resize改变图片分辨率，但是图片内容并不丢失，不是裁剪
        if way == 1:
            img_resize = img.resize((int(w*compress_rate), int(h*compress_rate)))
            resize_w, resieze_h = img_resize.size
            img_resize.save('result_' + self.img_name)
            if show:
                img_resize.show()  # 在照片应用中打开图片
                # 或
                # plt.imshow(img_resize)
                # plt.axis('off')
                # plt.show()

        # 方法二： 和resize方法类似，不过这里我测试好型这个函数已经不能使用，不知是不是版本问题
        # 问题：https://blog.csdn.net/kethur/article/details/79992539  tumbnail没有返回值
        if way == 2:
            # img_resize = img.thumbnail((400, 400))
            img.thumbnail((int(w*compress_rate), int(h*compress_rate)))
            resize_w, resize_h = img.size
            img.save('result2_' + self.img_name)
        print("%s 已压缩，" % (self.img_name), "压缩率：", compress_rate)