import logging
from typing import Any
from langchain_core.language_models import LLM
from langchain_core.messages import HumanMessage
from openai import OpenAI


# 自定义的包装器类继承langchain_core.language_models.LLM类
class Kimi(LLM):

    # llm 属性可不定义
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "kimillm"

    # 必须定义_call方法
    def _call(self, prompt: str, **kwargs: Any) -> str:

        try:

            client = OpenAI(
                # 此处请替换自己的api
                api_key="sk-ITwDE6ziZC6CD8aVGkMWSSNNSEJO2nzu4GHZ9Xdfc5TA03s9",
                base_url="https://api.moonshot.cn/v1",
            )
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[
                    {"role": "user", "content": prompt}
                ],

                temperature=0,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error in Kimi _call: {e}", exc_info=True)
            raise


# if __name__ == '__main__':
#     # 创建实例
#     llm = Kimi()
#
#     # 注意下面的 llm("你是谁")，这种调用方法LangChain 0.2.0已经移除，需要替换使用invoke方法
#     # llm("你是谁")
#
#     # 使用示例1
#     print(llm.invoke("你是谁"))
#
#     # 使用示例2：
#     llm = Kimi()
#
# instructions = """
#     你将得到一个带有水果名称的句子,提取这些水果名称并为其分配一个表情符号
#     在 python 字典中返回水果名称和表情符号
#     """
#
# fruit_names = """
#     苹果,梨,这是奇异果
#     """
#
# # 制作结合说明和水果名称的提示
# prompt = (instructions + fruit_names)
#
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)





