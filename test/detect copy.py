import pyautogui
import time

pyautogui.FAILSAFE = False

# 阶段配置（请确保图片路径正确）
stage_config = [
    {   # 第一阶段必须成功（设置基点）
        "image": "img1.jpg",
        "base_offset": (300, 0),
        "click_image": True
    },
    {
        "image": "img2.jpg", 
        "base_offset": (600, 0), 
        "click_image": True
    },
    {   # 后续阶段
        "image": "img2.jpg", 
        "base_offset": (300, -250), 
        "click_image": True
    },
    {
        "image": "img2.jpg", 
        "base_offset": (600, -250), 
        "click_image": True
    },
    {
        "image": "img2.jpg", 
        "base_offset": (600, -250), 
        "click_image": True
    }
]

base_point = None
current_stage = 0

def wait_until_found(image_path):
    """实时识别直到找到目标"""
    while True:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8, grayscale=True)
            if location:
                x, y = pyautogui.center(location)
                print(f"[识别成功] {image_path} ({x}, {y})")
                return (x, y)
            print(f"[扫描中] 等待识别：{image_path}...")
            time.sleep(0.8)  # 更快的扫描频率
        except Exception as e:
            print(f"[异常] {str(e)}")
            time.sleep(1)

try:
    while True:
        stage = stage_config[current_stage]
        print(f"\n—— 阶段 {current_stage} ——")
        
        # 阻塞式识别当前阶段图片
        img_pos = wait_until_found(stage["image"])
        
        # 点击识别到的图片
        if stage["click_image"]:
            pyautogui.click(img_pos)
            print(f"已点击图片坐标：{img_pos}")

        # 设置初始基点（仅第一阶段）
        if current_stage == 0:
            base_point = img_pos
            print(f"基点坐标已记录：{base_point}")

        # 执行基点偏移移动
        if base_point:
            target_x = base_point[0] + stage["base_offset"][0]
            target_y = base_point[1] + stage["base_offset"][1]
            pyautogui.moveTo(target_x, target_y)
            pyautogui.moveTo(target_x+1, target_y+1)
            print(f"已移动到偏移坐标：({target_x}, {target_y})")
            time.sleep(0.7)  # 移动后短暂停顿

        # 阶段切换逻辑
        current_stage += 1
        if current_stage >= len(stage_config):
            print("\n===== 完成循环 =====")
            current_stage = 0
            base_point = None
            time.sleep(1)  # 循环重置等待
        else:
            print("等待1秒进入下一阶段...")
            time.sleep(1)  # 阶段间等待

except KeyboardInterrupt:
    print("\n程序终止")