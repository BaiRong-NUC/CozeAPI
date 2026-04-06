import os
from dotenv import load_dotenv

# 获取工作空间列表
def get_space_list():
    pass

if __name__ == "__main__":
    load_dotenv() 
    COZE_API_KEY = os.environ.get("COZE_API_KEY")
    print(f"COZE_API_KEY: {COZE_API_KEY}")
    # # 获取工作空间列表
    # space_list = get_space_list()
    # print(space_list)