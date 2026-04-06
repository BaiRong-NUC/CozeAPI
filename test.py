import os
from dotenv import load_dotenv
from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL


# 获取工作空间列表
def get_space_list(coze: Coze):
    try:
        space_list = coze.workspaces.list()
        return space_list
    except Exception as e:
        print(f"获取工作空间列表失败: {e}")
        return None


if __name__ == "__main__":
    load_dotenv()
    COZE_API_KEY = os.environ.get("COZE_API_KEY")

    if not COZE_API_KEY:
        print("请设置环境变量 COZE_API_KEY")
        exit(1)

    # 初始化 Coze 客户端
    coze = Coze(
        # 声明令牌
        auth=TokenAuth(COZE_API_KEY),
        # 声明域名
        base_url=COZE_CN_BASE_URL,
    )

    # 获取工作空间列表
    space_list = get_space_list(coze)

    if space_list is not None:
        # print("工作空间列表:", space_list.items)
        for space in space_list.items:
            print(
                f"工作空间 ID: {space.id}, 名称: {space.name}, 类型: {space.workspace_type}"
            )
