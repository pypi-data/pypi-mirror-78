#!/usr/bin/python3
# -*- coding:utf-8 -*-
import re
import xmltodict
from collections import OrderedDict
from smart_tag_tools.LinqTool import linq
from smart_tag_tools.AuxiliaryManager import MyTreeClass


class FieldHandler:
    """
    适用结构：字典列表嵌套结构
    """

    @classmethod
    def update_field_value(cls, val, **fields):
        """
        修改字段值
        :param val:
        :param fields:
        :return:
        """
        if isinstance(val, dict):
            for field, v in fields.items():
                if field in val:
                    val[field] = v

            for key in val:
                cls.update_field_value(val[key], **fields)

        if isinstance(val, list):
            for item in val:
                cls.update_field_value(item, **fields)

    @classmethod
    def update_field_name(cls, val, **fields):
        """
        修改字段名
        :param val:
        :param fields:
        :return:
        """
        if isinstance(val, dict):
            for field, v in fields.items():
                if field in val:
                    val[v] = val.pop(field)

            for key in val:
                cls.update_field_name(val[key], **fields)

        if isinstance(val, list):
            for item in val:
                cls.update_field_name(item, **fields)

    @classmethod
    def remove_field(cls, val, *fields):
        """
        删除字段（递归）
        @param val:
        @param fields:
        @return:
        """
        if isinstance(val, dict):
            for field in fields:
                val.pop(field, "404")

            for key in val:
                cls.remove_field(val[key], *fields)

        if isinstance(val, list):
            for item in val:
                cls.remove_field(item, *fields)

    @classmethod
    def add_field(cls, val, **fields):
        """
        添加字段,只针对列表
        :param val:
        :param fields:
        :return:
        """

        if isinstance(val, list):
            for item in val:
                for field, v in fields.items():
                    item[field] = v


class MetadataConverter:
    """
    元数据结构字段调整
    """

    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.converts = xmltodict.parse(f.read())

    @staticmethod
    def prepare(data):
        for meta in data['metadatas']:
            if 'markmeta' in meta['type']:
                meta['type'] = 'model_sobey_object_markkeyframe'
                meta['name'] = 'model_sobey_object_markkeyframe'
                break

    def convert(self, meta, **kwargs):
        meta_type = meta['type']
        meta_type = meta_type[:-1].split('_')[-1] if meta_type.endswith('_') else meta_type.split('_')[-1]
        converter = linq(self.converts['collection']['field']).group_by('type').get(meta_type, [])
        for item in converter:
            before, after = item['before'], item['after']
            if before:
                if after:
                    FieldHandler.update_field_name(meta, before=after)
                else:
                    FieldHandler.remove_field(meta, before)
            else:
                FieldHandler.add_field(meta['metadata'], after=kwargs.get(after))


class ComConverter:
    @staticmethod
    def combine_to_heavy(items):
        """
        包含关系去重
        字幕去重/日期去重/地区名词去重/地区去重/头衔去重 ['广东省','广东省广州市']=>['广东省广州市']
        """
        length = len(items)
        for i in range(0, length):
            for j in range(i + 1, length):
                if items[i] in items[j]:
                    items[i] = '###'
                else:
                    items[j] = '###'
        return list(filter(lambda x: x != '###', items))

    @staticmethod
    def reporter_replace(items: list) -> list:
        """
        王斌(广东台记者/肇庆市人大常委会党组成员)--》王斌/记者、肇庆市人大常委会党组成员
        """

        def nj_replace_func(dic: dict) -> dict:
            k = '记者'
            if k in dic.get('name', ''):
                dic['name'] = dic['name'].replace('(敏感人物)', '###')
                name = dic['name'].split('(')[0].replace('###', '(敏感人物)')
                jobs = list(map(lambda x: k if k in x else x,
                                dic['name'].split('(')[1][:-1].split('/'))) if '(' in dic[
                    'name'] else []
                dic['name'] = '{}({})'.format(name, '/'.join(jobs))
            return dic

        return linq(items).select(lambda x: nj_replace_func(x)).distinct().tolist()

    @staticmethod
    def to_name_job(data: list) -> dict:
        """
        ['习近平(国家主席)','吴楠(CBA篮球运动员)']=>OrderedDict([(习近平, 国家主席),(吴楠, CBA篮球运动员)])
        """
        result = OrderedDict()
        if data:
            for tmp in data:
                job = list()
                tmp = tmp.replace('(敏感人物)', '###')
                if '(' in tmp:
                    job = re.search(r'.*(\(.*\)).*', tmp, re.S).group(1)[1:-1].split('/')
                result[tmp.split('(')[0].replace('###', '(敏感人物)')] = job
        return result

    @classmethod
    def duplicate_people(cls, x: list) -> list:
        """
        人脸去重（考虑头衔问题）
        ['习近平(国家主席)','习近平(中国共产党中央委员会总书记)']=>['习近平(国家主席/中国共产党中央委员会总书记)']
        """
        result = OrderedDict()
        if x:
            names = list()
            for tmp in x:
                tmp = tmp.replace('(敏感人物)', '###')
                name = tmp.split('(')[0].replace('###', '(敏感人物)')
                job = list()
                if '(' in tmp:
                    job = re.search(r'.*(\(.*\)).*', tmp, re.S).group(1)[1:-1].split('/')
                if name not in names:
                    names.append(name)
                    result[name] = job
                else:
                    result[name].extend(job)
        return ['{}({})'.format(k, '/'.join(cls.combine_to_heavy(v))) if v else k for k, v in result.items()]

    @classmethod
    def __intersection__(cls, x: list, y: list) -> list:
        """
        name取交集,相同人名的头衔合并
        """
        result = list()
        if x and y:
            x = cls.to_name_job(cls.duplicate_people(x))
            y = cls.to_name_job(cls.duplicate_people(y))
            for v in x.keys():
                if v in y.keys():
                    if x.get(v) or y.get(v):
                        job = '/'.join(cls.combine_to_heavy(x[v] + y[v]))
                        result.append('{name}({job})'.format(name=v, job=job))
                    else:
                        result.append('{name}'.format(name=v))
        return result

    @classmethod
    def __difference__(cls, x: list, y: list) -> list:
        """
        name取差集
        """
        result = list()
        if x:
            if not y:
                return x
            x = cls.to_name_job(cls.duplicate_people(x))
            y = cls.to_name_job(cls.duplicate_people(y))
            for v in x.keys():
                if v not in y.keys():
                    if x.get(v) or y.get(v):
                        result.append('{name}({job})'.format(name=v, job='/'.join(cls.combine_to_heavy(x[v]))))
                    else:
                        result.append('{name}'.format(name=v))
        return result

    @staticmethod
    def district__helper(data: list) -> list:
        """
        地区标签处理规则
        1.结合知识库查找地点对应地区，
        2.当地区标签个数=1时，直接返回为地区标签；
        3.当地区标签个数>1时，先按逻辑提取省，再提取省级下的市，再提取市级下的区，提取
        逻辑如下：
        取出现频次最高的省（/市/区）作为省级区域；
        特殊情况a.如果出现最高频次有多个省（/市/区）且频次不等于1则都保留
        情况b.如果出现所有省（/市/区）频次均为1则都舍弃
        情况c.如果只有1个省（/市/区）则保留。
        """
        if len(data) < 2:
            return data
        my_tree_class = MyTreeClass()
        district_tree = my_tree_class.tree()
        for row in data:
            my_tree_class.__node_add__(district_tree, row.split('/'))
        result = list()
        for tmp in data:
            filter_data = my_tree_class.__filter__(district_tree, tmp.split('/'))
            if filter_data not in result:
                result.append(filter_data)
        return result
