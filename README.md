#./detect
This is a new repository created using a script.

# 如何进入 Python 虚拟环境

1. 打开终端。
2. 导航到项目目录：
    ```sh
    cd /Users/wangxufeng/detect
    ```
3. 创建虚拟环境（如果尚未创建）：
    ```sh
    python3 -m venv venv
    ```
4. 激活虚拟环境：
    - 对于 macOS 和 Linux：
        ```sh
        source venv/bin/activate
        ```
    - 对于 Windows：
        ```sh
        .\venv\Scripts\activate
        ```
5. 现在你已经进入了虚拟环境，可以安装所需的依赖包：
    ```sh
    pip install -r requirements.txt
    ```

# 安装 OpenCV

如果你需要使用 `confidence` 参数，请安装 OpenCV：
```sh
pip install opencv-python
```
