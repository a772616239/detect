import pyautogui
import time

# 关闭自动防故障
pyautogui.FAILSAFE = False

# 图标截图路径（需提前截取图标保存为icon.jpg）
ICON_IMAGE = "icon.jpg"

# 定义分屏的区域 (左上角x, 左上角y, 宽度, 高度)
REGION = (0, 0, 1920, 1080)  # 例如：第一块屏幕的区域

try:
    while True:
        try:
            # 在屏幕指定区域内查找图标
            location = pyautogui.locateOnScreen(ICON_IMAGE, confidence=0.8, region=REGION)
            
            if location:
                # 计算图标中心点
                x, y = pyautogui.center(location)
                # 执行点击
                pyautogui.click(x, y)
                print(f"Clicked icon at ({x}, {y})")
            else:
                print("未找到图标，3秒后重试...")
        
        except NotImplementedError as e:
            print("需要安装 OpenCV 以使用 'confidence' 参数。")
            print("请运行以下命令安装 OpenCV：")
            print("pip install opencv-python")
            break
        
        except pyautogui.ImageNotFoundException:
            print("图标未找到，3秒后重试...")
        
        time.sleep(3)
except KeyboardInterrupt:
    print("\n程序已终止")
