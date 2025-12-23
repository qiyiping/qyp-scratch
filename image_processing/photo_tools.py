from PIL import Image, ImageDraw


def layout_2in_photos_on_6in(input_photo_path, output_photo_path):
    """
    将一张2寸照片排版到6寸相纸上（2x2布局，共4张）

    参数:
        input_photo_path (str): 输入原始照片的路径
        output_photo_path (str): 输出排版后照片的路径
    """
    try:
        # 第1步：打开并准备原始照片
        original_photo = Image.open(input_photo_path)

        # 第2步：将照片裁剪并缩放至标准2寸尺寸（413x579像素）
        # 智能裁剪函数，确保人物比例正确
        width_2in, height_2in = 413, 579
        cropped_photo = smart_crop(original_photo, width_2in, height_2in)
        # 缩放至精确尺寸
        standard_2in_photo = cropped_photo.resize((width_2in, height_2in), Image.LANCZOS)

        # 第3步：创建6寸相纸画布（白色背景）
        width_6in, height_6in = 1200, 1800
        canvas = Image.new('RGB', (width_6in, height_6in), (255, 255, 255))

        # 第4步：计算布局并粘贴照片
        # 定义照片间的间距
        padding = 20
        # 计算每张照片在画布上的起始位置
        start_x = (width_6in - (2 * width_2in + padding)) // 2  # 水平居中
        start_y = (height_6in - (3 * height_2in + 2 * padding)) // 3  # 垂直居中

        # 将标准2寸照片粘贴到画布
        positions = [
            (start_x, start_y),
            (start_x + width_2in + padding, start_y),
            (start_x, start_y + height_2in + padding),
            (start_x + width_2in + padding, start_y + height_2in + padding),
            (start_x, start_y + 2 * height_2in + 2 * padding),
            (start_x + width_2in + padding, start_y + 2 * height_2in + 2 * padding),
        ]

        for position in positions:
            canvas.paste(standard_2in_photo, position)

        # 第6步：保存排版好的图片
        canvas.save(output_photo_path, dpi=(300, 300))  # 设置输出DPI为300
        print(f"排版完成！文件已保存至：{output_photo_path}")

    except Exception as e:
        print(f"处理过程中出现错误：{e}")


def smart_crop(photo, target_width, target_height):
    """
    智能裁剪函数，按目标比例裁剪照片中心部分，避免人物变形

    参数:
        photo (PIL.Image): 原始照片对象
        target_width (int): 目标宽度
        target_height (int): 目标高度
    返回:
        PIL.Image: 裁剪后的照片对象
    """
    width, height = photo.size
    target_ratio = target_height / target_width
    photo_ratio = height / width

    # 根据原始照片与目标比例的关系进行裁剪
    if photo_ratio > target_ratio:
        # 照片“太高”，需要裁剪上下部分
        new_height = int(width * target_ratio)
        top = (height - new_height) // 2
        return photo.crop((0, top, width, top + new_height))
    else:
        # 照片“太宽”，需要裁剪左右部分
        new_width = int(height / target_ratio)
        left = (width - new_width) // 2
        return photo.crop((left, 0, left + new_width, height))


if __name__ == "__main__":
    import fire
    fire.Fire(layout_2in_photos_on_6in)
