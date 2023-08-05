# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-06-01 14:07:23
@LastEditTime: 2020-08-17 09:54:56
@LastEditors: HuangJingCan
@Description: 商品相关
"""

from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.machine.machine_info_model import *


class GoodsListHandler(TopBaseHandler):
    """
    @description: 导入商品列表(请求top接口)
    """
    def get_async(self):
        """
        @description: 导入商品列表(请求top接口)
        @param {type} 
        @return: 
        @last_editors: HuangJingCan
        """
        access_token = self.get_taobao_param().access_token
        goods_name = self.get_param("goods_name", "")
        page_index = int(self.get_param("page_index", 0))
        page_size = self.get_param("page_size", 10)
        order_tag = self.get_param("order_tag", "list_time")
        order_by = self.get_param("order_by", "desc")

        if self.get_is_test() == True:
            return self.reponse_json_success(self.test_goods_list())

        self.get_goods_list(page_index, page_size, goods_name, order_tag, order_by, access_token)


class GoodsInfoHandler(TopBaseHandler):
    """
    @description: 导入商品(请求top接口)
    """
    def get_async(self):
        """
        @description: 导入商品(请求top接口)
        @param {type} 
        @return: 
        @last_editors: HuangJingCan
        """
        access_token = self.get_taobao_param().access_token
        num_iid = self.get_param("goods_id")
        machine_id = self.get_param("machine_id", "0")
        is_check_machine_exist = int(self.get_param("is_check_exist", "0"))

        if self.get_is_test() == True:
            return self.reponse_json_success(self.test_goods_info())

        if is_check_machine_exist > 0:
            machine_info_model = MachineInfoModel()
            exist_machineed = machine_info_model.get_entity("goods_id=%s and id<>%s", params=[num_iid, machine_id])
            if exist_machineed:
                return self.reponse_json_error("ExistGoodsID", "对不起，当前商品ID已应用到其他盒子中")

        self.get_goods_info(num_iid, access_token)
