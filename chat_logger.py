import datetime

class ChatLogger:
    def __init__(self, filename="chat_log.txt"):
        self.filename = filename
        # ファイルを新規作成または既存のファイルを空にする
        open(self.filename, "w").close()

    def log(self, role, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {role}: {message}\n\n")

    def log_human(self, message):
        self.log("Human", message)

    def log_assistant(self, message):
        self.log("Assistant", message)

# ChatLoggerのインスタンスを作成
logger = ChatLogger()

# この時点から、チャットの内容が記録されます

print("チャットロガーが初期化されました。これ以降のチャット内容が記録されます。")