import time
import os
import base64
import uuid, json


def base64_save_img(img_base64, suffix='png', save_path="static/base64"):
    """
    :param img_base64: 图片base64编码，去掉编码头(data:image/png;base64)
    :param suffix: 生成本地图片的后缀
    :param save_path: 保存本地图片的路径
    :return: 返回图片路径
    """
    try:
        path = save_path + '/' + str(time.strftime("%Y-%m-%d", time.localtime()))
        # 判断路径是否存在，不存在就自动创建
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        filename = str(uuid.uuid4().hex) + '.' + suffix
        new_file_img = path + '/' + filename
        img_data = base64.b64decode(img_base64)
        with open(new_file_img, "wb") as f:
            f.write(img_data)
        return new_file_img
    except Exception as e:
        raise e


def write_json(file_name, data_dict):
    jsons = json.dumps(data_dict, sort_keys=True, indent=4, separators=(',', ': '))
    with open(file_name, 'a+') as f:
        f.write(jsons)
        f.writelines(",")
        f.writelines("\n")
