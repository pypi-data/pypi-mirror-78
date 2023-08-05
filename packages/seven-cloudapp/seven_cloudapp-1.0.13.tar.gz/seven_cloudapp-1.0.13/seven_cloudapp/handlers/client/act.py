# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-05-26 15:26:32
@LastEditTime: 2020-08-11 17:52:52
@LastEditors: HuangJingCan
@Description: 活动处理
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.seven_model import PageInfo
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *
import decimal


class ActInfoHandler(SevenBaseHandler):
    """
    @description: 获取活动信息
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):
        act_id = self.get_param('act_id')

        app_id = self.get_taobao_param().source_app_id

        app_info_model = AppInfoModel()
        app_info = app_info_model.get_entity("app_id=%s", params=app_id)
        if not app_info:
            return self.reponse_json_error("NoApp", "对不起，找不到该小程序")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("app_id=%s and id=%s", params=[app_id, act_id])
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，找不到该活动")

        act_info.store_id = app_info.store_id

        self.reponse_json_success(act_info)


class MachinieListHandler(SevenBaseHandler):
    """
    @description: 机台列表
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取机台列表
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        app_id = self.get_taobao_param().source_app_id
        act_id = int(self.get_param("act_id", "0"))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        machine_info_model = MachineInfoModel()
        condition = "act_id=%s AND app_id=%s AND is_release=1"
        machine_info_page_list, total = machine_info_model.get_dict_page_list("*", page_index, page_size, condition, order_by="sort_index desc", params=[act_id, app_id])

        page_info = PageInfo(page_index, page_size, total, machine_info_page_list)

        self.reponse_json_success(page_info)


class PrizeListHandler(SevenBaseHandler):
    """
    @description: 奖品列表
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):
        """
        @description:  获取奖品列表
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        app_id = self.get_taobao_param().source_app_id
        act_id = int(self.get_param("act_id", "0"))
        machine_id = int(self.get_param("machine_id", "0"))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        act_prize_model = ActPrizeModel()
        condition = "act_id=%s AND machine_id=%s AND is_release=1"
        field = "id,act_id,award_id,app_id,owner_open_id,machine_id,prize_name,prize_title,prize_pic,prize_detail,goods_id,goods_code,goods_code_list,prize_type,prize_price,surplus,is_surplus,prize_total,tag_id,is_sku,sort_index,create_date"
        act_prize_page_list, total = act_prize_model.get_dict_page_list(field, page_index, page_size, condition, order_by="sort_index desc", params=[act_id, machine_id])
        page_info = PageInfo(page_index, page_size, total, act_prize_page_list)

        self.reponse_json_success(page_info)