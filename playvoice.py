import streamlit as st
from gtts import gTTS
import io
import base64
import time

# Streamlit アプリケーション
st.title("テキスト音声変換アプリ")

# ユーザーが入力するテキスト
text = st.text_area("テキストを入力してください:")

# 特定の略語を手動で調整
if text:
    text = text.replace("RS", "アールエス")

# テキストが入力された場合、音声に変換する
if st.button("音声を再生"):
    if text:
        # gTTS を使って音声に変換
        tts = gTTS(text, lang='ja')
        
        # BytesIOを使って音声データをメモリ上に保存
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        
        # バッファの先頭に戻る
        audio_buffer.seek(0)

        # BytesIOオブジェクトからバイトデータを取得
        audio_bytes = audio_buffer.getvalue()

        # Base64エンコードしてHTMLで埋め込むための文字列に変換
        audio_placeholder = st.empty()
        audio_str = "data:audio/ogg;base64,%s" % base64.b64encode(audio_bytes).decode()
        audio_html = """
                    <audio autoplay=True>
                    <source src="%s" type="audio/ogg" autoplay=True>
                    Your browser does not support the audio element.
                    </audio>
                """ % audio_str

        audio_placeholder.empty()
        time.sleep(0.5)  # これがないと上手く再生されません
        audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

        # 音声ファイルを再生
        st.audio(audio_buffer, format="audio/mp3")
    else:
        st.write("テキストを入力してください。")
