# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import dataframe_image as dfi

from rasa_sdk.events import SlotSet
import csv
import requests
import json
import re

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

class Compareschools(Action):
    def name(self) -> Text:
        return "answer_compare_schools"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 检查必填槽位
        schools=tracker.get_slot(key='school')
        schools=','.join(schools)

        dispatcher.utter_message(schools)

        return []

def score_prob(num, place, subject, mode):
    prob_df=pd.read_csv(f'{mode}.csv',encoding='utf-8')
    data=prob_df[(prob_df['地区']==place) & (prob_df['科类代表数字']==subject)]
    prob_list=[]
    for i in range(len(data)):
        min_score=data.iloc[i,-1]
        max_score=data.iloc[i,-2]
        prob=(num-min_score)/(max_score-min_score)#归一化
        if prob>1:
            prob=1
        elif prob<0:
            prob=0
        prob_list.append(prob)
    data['概率']=prob_list
    #调整返回格式

    data=data[['地区','专业名称','科类','批次','调整最高','调整最低','概率']].rename(columns={'调整最高':'预测最高','调整最低':'预测最低'})
    data=data.sort_values(by='概率',ascending=True, inplace=False, na_position='first')
    data.reset_index(inplace=True, drop=True)
    # return data
    dfi.export(obj=data, filename=f'{mode}.jpg')

class recommend_uibe_discipline(Action):
    def name(self) -> Text:
        return "answer_recommend_uibe_discipline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 检查必填槽位
        if tracker.slots['num'] == None:
            dispatcher.utter_message("输入的数字无效，请告诉我您的排名或者分数")
            return [
                # UserUtteranceReverted()
            ]
        else:
            try:
                num = int(tracker.slots['num'])
                # 将实体值赋给槽位
                tracker.slots["num"] = num
            except ValueError:
                dispatcher.utter_message("请告诉我您的排名或者分数")
                return [
                    # UserUtteranceReverted()
                ]


        if tracker.slots['mode'] == None:
            dispatcher.utter_message("请告诉我推荐专业的方式是分数还是排名")
            return [
                # UserUtteranceReverted()
            ]
        else:
            try:
                mode = tracker.slots['mode']
                # 将实体值赋给槽位
            except ValueError:
                dispatcher.utter_message("请告诉我您选择推荐专业的方式是分数还是排名")
                return [
                    # UserUtteranceReverted()
                ]

        if tracker.slots['category'] == None:
            dispatcher.utter_message("输入科目类别无效，请问您想查询的分科类别为理科、文科、历史类、物理类还是综合改革？")
            return [
                # UserUtteranceReverted()
            ]
        else:
            if tracker.slots['category']=='文科' or tracker.slots['category']=='历史类':
                subject = 1
            elif tracker.slots['category']=='理科' or tracker.slots['category']=='物理类':
                subject = 2
            elif tracker.slots['category'] == '综合改革':
                subject = 3
            else:
                dispatcher.utter_message("请问您想查询的是分科类别为理科、文科、历史类、物理类还是综合改革？")
                return [
                    # UserUtteranceReverted()
                ]

        if tracker.slots['place'] == None:
            dispatcher.utter_message("输入生源地无效，请问您的生源地省份是？")
            return [
                # UserUtteranceReverted()
            ]
        else:
            try:
                place = tracker.slots['place']
                if place in ['北京','天津','上海','海南']:
                    dispatcher.utter_message("抱歉北京,天津,上海,海南目前没有数据")
                    return []
                # 将实体值赋给槽位
            except ValueError:
                dispatcher.utter_message("请告诉我您的生源地省份")
                return [
                    # UserUtteranceReverted()
                ]

        dispatcher.utter_message('推荐贸大专业结果请查看{}.jpg'.format(mode))
        score_prob(num, place, subject, mode)


        return []


class DisciplineEntitiesAction(Action):
    def name(self):
        return "action_extract_discipline"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # 创建近义词匹配字典sym
        sym = {}
        with open('C:\\Users\\LJH\\Desktop\\chat_bot\\Rasa\\近义词-正向.csv', 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                for i in range(1, len(row)):
                    if row[i] != '':
                        if row[i] in sym:
                            sym[row[i]].append(row[0])
                        else:
                            sym[row[i]] = [row[0]]

        # 获取最近一条消息中所有被（多种分类器）提取的所有实体
        entity_list = tracker.latest_message.get("entities", [])
        for item in entity_list:
            # 检查entity为”discipline"且extractor为RegexEntityExtractor的字典
            if item.get('entity') == 'discipline' and item.get('extractor') == 'RegexEntityExtractor':
                # 正则提取成功
                extracted_value = item.get('value')  # 提取value到新的变量

                final_values = sym[extracted_value]  # 近似匹配的结果列表
                if len(final_values) == 1:
                    # 只有一个结果
                    return [SlotSet("discipline", final_values[0])]
                else:
                    # 多个结果，询问用户究竟要问哪个专业
                    message = "您要查询的专业是："
                    for value in final_values:
                        message += value + "/"
                    dispatcher.utter_message(text=message)
                    # 先把extracted_value放到槽里，经过下一轮用户对话再确定究竟要问哪个
                    return [SlotSet("discipline", extracted_value)]

        # 正则没提取到，看DIET是否提取到
        for item in entity_list:
            if item.get('entity') == 'discipline' and item.get('extractor') == 'DIETClassifier':
                extracted_value += item.get('value')

                final_values = char_sym(extracted_value)  # 近似匹配的结果列表
                if len(final_values) == 1:
                    # 只有一个结果
                    return [SlotSet("discipline", final_values[0])]
                else:
                    # 多个结果，询问用户究竟要问哪个专业
                    message = "您要查询的专业是："
                    for value in final_values:
                        message += value + "/"
                    dispatcher.utter_message(text=message)
                    # 先把extracted_value放到槽里，经过下一轮用户对话再确定究竟要问哪个
                    return [SlotSet("discipline", extracted_value)]

        # DIET也没提取到
        message = "未查找到您查询的专业信息"
        dispatcher.utter_message(text=message)
        return []


class DisciplineEntitiesAction(Action):
    def name(self):
        return "reply_jiuye"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/cqky2sy7ebaj63ak/?access_token=" + get_access_token()

        payload = json.dumps({
            "query": tracker.latest_message['text'],
            "plugins": ["uuid-zhishiku"],
            "verbose": True
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        string = response.text

        match = re.search(r"result\":\".*?\",\"is_truncated\":false", string)

        if match:
            start = match.start()
            end = match.end()

            dispatcher.utter_message(string[start + 9:end - 22])
        return []


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=pGRnDoNGZBOdfRGFPUaem4yE&client_secret=e8jLFqo0YHTsr8G6gSYMYkfpg6ixa8QH"
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def char_in(string1, string2):
    # 检测字符串string1的字符在字符串string2中出现的个数
    num = 0
    for char in string1:
        if char in string2:
            num += 1
    return num


def char_sym(string1, dict):
    count_dict = {}
    for key in dict:
        count_dict[key] = char_in(string1, key)
    max_count = max(count_dict.values())
    key_with_max_count = [key for key, value in count_dict.items() if value == max_count]
    if max_count == 0:
        # 无重复字符匹配项
        return ([])
    if len(key_with_max_count) <= 3:
        # 最相似的个数小于等于3
        result = []
        for key in dict:
            if key in key_with_max_count:
                result.extend(dict[key])
        return list(set(result))

        # 有很多匹配项，也算没找到
    return ([])


class Answer_Admission_Line(Action):
    def name(self) -> Text:
        return "reply_admission_line"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        discipline = tracker.slots['discipline']
        message = str(discipline) + "专业的历年分数线波动如下："
        dispatcher.utter_message(text=message)

        return []