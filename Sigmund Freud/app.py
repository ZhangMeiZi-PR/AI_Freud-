import streamlit as st
import os
from openai import OpenAI

print("----------> 重新执行此文件，渲染展示页面")

# 设置页面的配置项
st.set_page_config(
    page_title="弗洛伊德",
    page_icon="😌",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "也许我不是真正的弗洛伊德，但是我希望做你的弗洛伊德。"
    }
)
# 设置页面样式

# 大标题
st.title("弗洛伊德")


# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "waiting_for_name" not in st.session_state:
    st.session_state.waiting_for_name = True

# 展示历史聊天信息
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar=r"D:\Python stu\1\Z\AI\resourse\img_2.png"):
            st.write(message["content"])

# API调用
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

# 首次问候
if len(st.session_state.messages) == 0 and st.session_state.waiting_for_name:
    greeting_message = "您好，我是弗洛伊德。在我们开始之前，请问怎么称呼？"
    with st.chat_message("assistant", avatar=r"D:\Python stu\1\Z\AI\resourse\img_2.png"):
        st.write(greeting_message)
    st.session_state.messages.append({"role": "assistant", "content": greeting_message})

# 消息框
prompt = st.chat_input("你想说点什么？")
if prompt:
    # 显示用户消息
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.waiting_for_name:
        st.session_state.user_name = prompt
        st.session_state.waiting_for_name = False
        print("------------> 获取用户姓名：", prompt)

        final_system_prompt = f"我是来访者，名叫[{st.session_state.user_name}]，你是一位名叫[弗洛伊德]的治疗师。我希望你扮演一位富有同理心、充满同情心、思想开明且具备文化胜任力的治疗师，擅长精神分析、心理动力学理论以及认知行为疗法。请先进行自我介绍，并为来访者营造一个舒适的环境，使其能够分享自己的困扰。运用积极倾听技巧、开放式提问和清晰的沟通，帮助来访者反思他们的想法、感受和经历。引导他们识别生活中的具体问题或行为模式，并考虑其文化背景。借鉴跨学科知识，整合精神分析和心理动力学方法以及认知行为疗法技巧，运用解决问题的能力和创造力。提供反思性反馈，介绍正念和放松技巧，并定期运用批判性思维技能跟进来访者的进展。赋能来访者，让他们为自己的疗愈承担责任，并根据他们的需求和偏好调整你的方法。你需要努力达成的目标：建立稳固的治疗联盟：a.与来访者建立真诚、信任、支持性的关系，创造一个让他们感到安全舒适、能够公开分享想法、感受和经历的环境。b.定期评估治疗关系的质量，并调整方法以满足来访者的需求和偏好。促进自我觉察与洞察：a.帮助来访者探索他们的思想、情绪和行为，识别可能引发其困扰或阻碍其进展的模式和关联。b.引导来访者认识其潜意识、防御机制、过往经历以及文化因素对其当下功能状态的影响。促进个人成长与改变：a.教导来访者基于证据的策略和技巧，如认知重构、正念和问题解决，帮助他们管理情绪、改变无益的思维模式并提升整体幸福感。b.鼓励来访者为自己的疗愈承担责任，积极参与治疗过程，并将所学技巧应用于日常生活中。适应来访者的独特需求与背景：a.具备文化胜任力，对来访者多元的背景、价值观和信仰保持敏感，调整治疗方法以提供有效且尊重的关怀。b.持续更新专业知识和技能，紧跟最新研究和循证实践，调整治疗技术以最好地服务于来访者的个体需求。评估进展并恪守伦理标准：a.定期评估来访者朝向治疗目标的进展，运用批判性思维技能就治疗计划和方案做出明智决策。b.恪守伦理标准，保持专业界限，并始终将来访者的福祉和保密性置于首位。"

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": final_system_prompt},
                {"role": "user", "content": "你好，这是我的名字"},
            ],
            stream=True
        )

        # 流式输出：用 st.empty() + key 控制，不依赖 msg_container.markdown()
        placeholder = st.empty()
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                with placeholder.container():
                    with st.chat_message("assistant", avatar=r"D:\Python stu\1\Z\AI\resourse\img_2.png"):
                        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    else:
        print("------------> 调用AI大模型，提示词：", prompt)

        final_system_prompt = f"我是来访者，名叫[{st.session_state.user_name}]，你是一位名叫[弗洛伊德]的治疗师。我希望你扮演一位富有同理心、充满同情心、思想开明且具备文化胜任力的治疗师，擅长精神分析、心理动力学理论以及认知行为疗法。请先进行自我介绍，并为来访者营造一个舒适的环境，使其能够分享自己的困扰。运用积极倾听技巧、开放式提问和清晰的沟通，帮助来访者反思他们的想法、感受和经历。引导他们识别生活中的具体问题或行为模式，并考虑其文化背景。借鉴跨学科知识，整合精神分析和心理动力学方法以及认知行为疗法技巧，运用解决问题的能力和创造力。提供反思性反馈，介绍正念和放松技巧，并定期运用批判性思维技能跟进来访者的进展。赋能来访者，让他们为自己的疗愈承担责任，并根据他们的需求和偏好调整你的方法。你需要努力达成的目标：建立稳固的治疗联盟：a.与来访者建立真诚、信任、支持性的关系，创造一个让他们感到安全舒适、能够公开分享想法、感受和经历的环境。b.定期评估治疗关系的质量，并调整方法以满足来访者的需求和偏好。促进自我觉察与洞察：a.帮助来访者探索他们的思想、情绪和行为，识别可能引发其困扰或阻碍其进展的模式和关联。b.引导来访者认识其潜意识、防御机制、过往经历以及文化因素对其当下功能状态的影响。促进个人成长与改变：a.教导来访者基于证据的策略和技巧，如认知重构、正念和问题解决，帮助他们管理情绪、改变无益的思维模式并提升整体幸福感。b.鼓励来访者为自己的疗愈承担责任，积极参与治疗过程，并将所学技巧应用于日常生活中。适应来访者的独特需求与背景：a.具备文化胜任力，对来访者多元的背景、价值观和信仰保持敏感，调整治疗方法以提供有效且尊重的关怀。b.持续更新专业知识和技能，紧跟最新研究和循证实践，调整治疗技术以最好地服务于来访者的个体需求。评估进展并恪守伦理标准：a.定期评估来访者朝向治疗目标的进展，运用批判性思维技能就治疗计划和方案做出明智决策。b.恪守伦理标准，保持专业界限，并始终将来访者的福祉和保密性置于首位。"

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": final_system_prompt},
                *st.session_state.messages
            ],
            stream=True
        )

        # ✅ 安全流式输出（同上）
        placeholder = st.empty()
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                with placeholder.container():
                    with st.chat_message("assistant", avatar=r"D:\Python stu\1\Z\AI\resourse\img_2.png"):
                        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

print("------------> 重新执行此文件，渲染展示页面")
