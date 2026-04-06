# CozeAPI

用于测试 [Coze](https://www.coze.cn) 低代码平台下的 API 与 SDK 功能。

## 项目简介

本项目基于 Python，通过调用 Coze 开放平台提供的 REST API 及官方 SDK，对其核心功能进行测试与验证，包括但不限于：

- 工作空间（Space）管理
- Bot 创建与发布
- 对话（Conversation）与消息（Message）接口
- 工作流（Workflow）调用

## 环境要求

- Python 3.8+
- Coze 账号及 API Token

## 快速开始

1. 克隆项目

    ```bash
    git clone https://gitee.com/BaiRong-NUC/CozeApi.git
    cd CozeApi
    ```

2. 安装依赖

    ```bash
    pip install cozepy
    ```

3. 配置 API Token

    在环境变量或代码中设置你的 Coze Personal Access Token：

    ```bash
    set COZE_API_TOKEN=your_token_here
    ```

4. 运行测试

    ```bash
    python test.py
    ```

## 参考文档

- [Coze 开放平台文档](https://www.coze.cn/docs)
- [cozepy SDK](https://github.com/coze-dev/coze-py)
