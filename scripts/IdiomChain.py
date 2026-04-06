import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL, Message, ChatStatus, MessageType
from datetime import datetime

# 调用成语接龙智能体DEMO

load_dotenv()
app = Flask(__name__)
CORS(app)  # 启用CORS支持


class IdiomChain:
    def __init__(self):
        self.api_token = os.environ.get("COZE_API_KEY")  # str
        self.bot_id = os.environ.get("IDIOM_CHAIN_BOT_ID")  # str
        self.user_id = os.environ.get("USER_ID")  # str

        self.current_idiom = None  # 当前成语
        self.idioms_history = []  # 成语历史记录
        self.conversation_id = None  # 当前会话ID

        # 初始化 Coze 客户端
        self.coze = Coze(
            auth=TokenAuth(self.api_token),
            base_url=COZE_CN_BASE_URL,
        )

    def reset(self):
        """重置游戏状态"""
        self.current_idiom = None
        self.idioms_history = []
        self.conversation_id = None

    def play(self, user_input: str):
        try:
            # 构建消息对象
            message = Message(
                role="user",
                content=user_input,
                content_type="text",
                type="question",
            )

            # 调用智能体接口
            # 如果有conversation_id，继续之前的会话；否则创建新会话
            if self.conversation_id:
                response = self.coze.chat.create(
                    bot_id=self.bot_id,
                    user_id=self.user_id,
                    conversation_id=self.conversation_id,
                    additional_messages=[message],
                    auto_save_history=True,
                )
            else:
                response = self.coze.chat.create(
                    bot_id=self.bot_id,
                    user_id=self.user_id,
                    additional_messages=[message],
                    auto_save_history=True,
                )
                # 保存新会话的ID
                self.conversation_id = response.conversation_id

            # 等待结果
            while response.status == ChatStatus.IN_PROGRESS:
                response = self.coze.chat.retrieve(
                    conversation_id=response.conversation_id, chat_id=response.id
                )

            sdk_response = None
            if response.status == ChatStatus.COMPLETED:
                coze_message = self.coze.chat.messages.list(
                    conversation_id=response.conversation_id, chat_id=response.id
                )
                for msg in coze_message.data:
                    if (
                        hasattr(msg, "role")
                        and msg.role == "assistant"
                        and msg.type == MessageType.ANSWER
                    ):
                        # print(f"智能体回复: {msg}")
                        sdk_response = msg.content

            return sdk_response

        except Exception as e:
            print(f"调用成语接龙智能体失败: {e}")
            return None


idiom_chain = IdiomChain()


@app.route("/idioms/play", methods=["POST"])
def play_idiom_chain():
    data = request.get_json(silent=True) or {}
    user_input = data.get("user_input", "")

    if not user_input:
        return jsonify({"error": "缺少 user_input"}), 400

    result = idiom_chain.play(user_input)
    if result is None:
        return jsonify({"error": "调用智能体失败"}), 500

    return jsonify(
        {
            "status": "success",
            "reply": result,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
    )


@app.route("/idioms/reset", methods=["POST"])
def reset_idiom_chain():
    """重置游戏，开始新的会话"""
    idiom_chain.reset()
    return jsonify(
        {
            "status": "success",
            "message": "游戏已重置",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
