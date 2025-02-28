
import pyautogui
import time
import pyperclip
import ImgAll
import SaveReadingData
pyautogui.FAILSAFE = False

stage_config = [
    {   # 第一阶段必须成功（设置基点）
        "image": "img1.jpg",
        "base_offset": (600, -250),
        "click_image": True,
        "timeout": 28
    },
    {   # 后续阶段
        "image": "img2.jpg", 
        "base_offset": (300, -250), 
        "click_image": True
    },
    {
        "image": "img2.jpg", 
        "base_offset": (300, 0), 
        "click_image": True
    },
    {
        "image": "img2.jpg", 
        "base_offset": (600, 0), 
        "click_image": True
    },
    {
        "image": "img2.jpg", 
        "base_offset": (600, 0), 
        "click_image": True
    },
    {
        "image": "img4.jpg", 
        "base_offset": (600, -250), 
        "click_image": True,
        "timeout": 1
    },
    {   # 新增阶段：识别img3并操作输入框
        "image": "img3.jpg",
        "click_image": False,
        "click_offset": (100, 200),
        "keyboard_actions": ["ctrl+a", "ctrl+v"],
        
    }
]
fscale=1
filename = SaveReadingData.filename
base_point = None
current_stage = 0
times=0
arrIndex=0
arrIndex = SaveReadingData.load_data(filename)+1
print(f"arrIndex:{arrIndex}")

def scale_position(pos):
    """将坐标缩放为fscale倍以适应Retina屏幕"""
    return (int(pos[0] * fscale), int(pos[1] * fscale))

def wait_until_found(image_path, timeout=None):
    """实时识别直到找到目标或超时"""
    start_time = time.time()
    while True:
        try:
            if timeout is not None and time.time() - start_time >= timeout:
                print(f"[超时] {timeout}秒内未找到图片：{image_path}")
                return None
            location = pyautogui.locateOnScreen(image_path, confidence=0.8, grayscale=True)
            if location:
                x, y = pyautogui.center(location)
                scaled_pos = scale_position((x, y))  # 坐标缩放
                print(f"[识别成功] {image_path} ({scaled_pos[0]}, {scaled_pos[1]})")
                return scaled_pos
            print(f"[扫描中] 等待识别：{image_path}...")
            time.sleep(1.8)
        except Exception as e:
            print(f"[异常] {str(e)}")
            time.sleep(2)

try:
    while True:
        stage = stage_config[current_stage]
        print(f"\n—— 阶段 {current_stage} ——")
        timeout=20
        if stage.get("timeout", None):
            timeout = stage["timeout"]
            
        # 根据阶段设置超时时间
        if current_stage == 0:
            img_pos = wait_until_found(stage["image"])
        else:
            img_pos = wait_until_found(stage["image"], timeout=timeout)
        
        if img_pos is None:
            print(f"阶段 {current_stage} 识别超时，进入下一阶段。")
            current_stage += 1
            if current_stage >= len(stage_config):
                print("\n===== 完成循环 =====")
                current_stage = 0
                base_point = None
                time.sleep(2)
            continue
        
        # 点击图片位置
        if stage.get("click_image", False):
            pyautogui.click(img_pos)
            print(f"已点击图片坐标：{img_pos}")

        # 执行偏移点击操作
        if "click_offset" in stage:
            # 缩放偏移量
            offset_x, offset_y = stage["click_offset"]
            offset_x = int(offset_x * fscale)
            offset_y = int(offset_y * fscale)
            target_x = img_pos[0] + offset_x
            target_y = img_pos[1] + offset_y
            pyautogui.click(target_x, target_y)
            print(f"已点击偏移坐标：({target_x}, {target_y})")
            time.sleep(1)  # 确保输入框获得焦点

        # 设置初始基点（仅第一阶段）
        if current_stage == 0:
            base_point = img_pos
            print(f"基点坐标已记录：{base_point}")

        # 执行基点偏移移动
        if base_point and "base_offset" in stage:
            # 缩放偏移量
            offset_x, offset_y = stage["base_offset"]
            offset_x = int(offset_x * fscale)
            offset_y = int(offset_y * fscale)
            target_x = base_point[0] + offset_x
            target_y = base_point[1] + offset_y
            pyautogui.moveTo(target_x, target_y)
            pyautogui.moveTo(target_x+1, target_y+1)
            print(f"已移动到偏移坐标：({target_x}, {target_y})")
            time.sleep(1.7)

        # 执行键盘操作（无需坐标调整）
        if "keyboard_actions" in stage:
            print("执行键盘操作：", stage["keyboard_actions"])
            # 加载数据
            arrIndex = SaveReadingData.load_data(filename)
            print(f"arrIndex:{arrIndex}")
            if times<3:
                times+=1
            else:
                times=0
                arrIndex+=1
                # 保存数据
                SaveReadingData.save_data(arrIndex, filename)

            strContent=ImgAll.ImgArr[arrIndex]["description"]
            print(strContent)
            pyperclip.copy(strContent)
            for action in stage["keyboard_actions"]:
                if action == "ctrl+a":
                    pyautogui.hotkey('command', 'a')
                elif action == "ctrl+v":
                    pyautogui.hotkey('command', 'v')
                time.sleep(0.6)

        # 阶段切换
        current_stage += 1
        if current_stage >= len(stage_config):
            print("\n===== 完成循环 =====")
            current_stage = 0
            base_point = None
            time.sleep(2)
        else:
            print("等待1秒进入下一阶段...")
            time.sleep(1)

except KeyboardInterrupt:
    print("\n程序终止")