# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class AnswerSchoolLevel(Action):
    def name(self) -> Text:
        return "answer_school_level"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = ("对外经济贸易大学是教育部直属的顶尖211大学\n"
                   "是国家首批“211 工程”和首批“双一流”建设高校\n"
                   "也是新中国成立的第一所财经类全国重点大学"
                   )
        dispatcher.utter_message(text=message)
        return []

class AnswerSchoolLocation(Action):
    def name(self) -> Text:
        return "answer_school_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ("对外经济贸易大学位于北京市朝阳区惠新东街10号，属于北三环\n"
                   "在北京地铁十号线芍药居站、惠新西街南口站附近\n"
                   "紧邻奥林匹克公园，靠近国贸、三里屯、望京等繁华商业中心")

        dispatcher.utter_message(text=message)
        return []

class AnswerSchoolTraffic(Action):
    def name(self) -> Text:
        return "answer_school_traffic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ("学校附近相距较近的地铁站有惠新西街南口站和芍药居站\n"
                   "公交站有对外经贸大学东门站，对外经贸大学站,中国现代文学馆站\n"
                   "详细乘车路线可以使用地图APP推荐出行方案")

        dispatcher.utter_message(text=message)
        return []

class AnswerSchoolPolicy(Action):
    def name(self) -> Text:
        return "answer_school_policy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ("可参考我校招生网http://zhaosheng.uibe.edu.cn/主页,包含最新的招生政策\n"
                   "欢迎报考对外经济贸易大学！")

        dispatcher.utter_message(text=message)
        return []