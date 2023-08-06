# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-02 13:44:17
@LastEditTime: 2020-08-26 15:49:03
@LastEditors: HuangJingCan
@Description: 奖品相关
"""
from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.throw.throw_goods_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.seven_model import *
from seven_cloudapp.models.enum import *

from seven_cloudapp.libs.customize.seven import *


class PrizeListHandler(SevenBaseHandler):
    """
    @description: 奖品列表
    """
    @filter_check_params("machine_id")
    def get_async(self):
        """
        @description: 奖品列表
        @param {type} 
        @return: 
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", "0"))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))
        machine_id = int(self.get_param("machine_id", "0"))
        field = "id,sort_index,prize_pic,prize_name,prize_price,probability,prize_limit,surplus,tag_id,is_sku,is_release,is_surplus,prize_detail,goods_code,goods_code_list,goods_id,force_count,lottery_type"
        condition = "machine_id=%s"

        if machine_id <= 0:
            return self.reponse_json_error_params()

        act_prize_model = ActPrizeModel()

        # 奖品总件数
        prize_all_count = act_prize_model.get_total("machine_id=%s", params=machine_id)
        # 库存不足奖品件数
        prize_surplus_count = act_prize_model.get_total("machine_id=%s AND surplus=0", params=machine_id)
        # 可被抽中奖品件数
        prize_lottery_count = act_prize_model.get_total("machine_id=%s AND probability>0 AND surplus>0 AND is_release=1", params=machine_id)
        #奖品总权重
        sum_probability = act_prize_model.get_dict("machine_id=%s and is_release=1", field="sum(probability) as probability", params=machine_id)

        page_list, total = act_prize_model.get_dict_page_list(field, page_index, page_size, condition, "", "sort_index desc", params=machine_id)

        #强制命中信息
        must_prize_list = [must_prize for must_prize in page_list if must_prize["force_count"] > 0]
        prize_roster_model = PrizeRosterModel()
        prize_roster_total = prize_roster_model.get_total("machine_id=%s", params=machine_id)

        cur_prize_info_list2 = []

        for i in range(0, len(must_prize_list)):
            page_total = int(prize_roster_total / must_prize_list[i]["force_count"])
            prize_roster_after_list = prize_roster_model.get_dict_list("machine_id=%s", "", "id asc", str(page_total * must_prize_list[i]["force_count"]) + "," + str((page_total * must_prize_list[i]["force_count"]) + must_prize_list[i]["force_count"]), params=machine_id)
            area_must_count = must_prize_list[i]["force_count"]
            is_exist = 0
            if (len(prize_roster_after_list) > 0):
                prize_roster_after_list.reverse()
                for j in range(0, len(prize_roster_after_list)):
                    if prize_roster_after_list[j]["prize_id"] == must_prize_list[i]["id"]:
                        is_exist = 1
                        area_must_count = must_prize_list[i]["force_count"] - len(prize_roster_after_list)
                        sum_probability["probability"] = int(sum_probability["probability"]) - must_prize_list[i]["probability"]
                        break
                    else:
                        area_must_count += -1

            must_prize_list[i]["area_must_count"] = area_must_count
            must_prize_list[i]["is_area_selected"] = is_exist

        page_list = SevenHelper.merge_dict_list(page_list, "id", must_prize_list, "id", "area_must_count,is_area_selected")

        for i in range(len(page_list)):
            page_list[i]["prize_detail"] = json.loads(page_list[i]["prize_detail"])
            if page_list[i]["goods_code_list"] == "":
                page_list[i]["goods_code_list"] = "[]"
            page_list[i]["goods_code_list"] = json.loads(page_list[i]["goods_code_list"])

        page_info = PageInfo(page_index, page_size, total, page_list)
        page_info.prize_all_count = prize_all_count
        page_info.prize_surplus_count = prize_surplus_count
        page_info.prize_lottery_count = prize_lottery_count
        if sum_probability["probability"]:
            page_info.prize_sum_probability = int(sum_probability["probability"])
        else:
            page_info.prize_sum_probability = 0

        self.reponse_json_success(page_info)


class PrizeDelHandler(SevenBaseHandler):
    """
    @description: 删除奖品
    """
    @filter_check_params("prize_id")
    def get_async(self):
        """
        @description: 删除奖品
        @param prize_id：奖品id
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        prize_id = int(self.get_param("prize_id", "0"))

        if prize_id <= 0:
            return self.reponse_json_error_params()

        act_prize_model = ActPrizeModel()
        act_prize = act_prize_model.get_entity("id=%s", params=prize_id)

        if not act_prize:
            return self.reponse_json_success()

        act_prize_model.del_entity("id=%s", prize_id)

        #投放商品处理
        self.throw_goods_update(act_prize)

        self.create_operation_log(OperationType.delete.value, "act_prize_tb", "PrizeDelHandler", None, prize_id)

        self.reponse_json_success()

    def throw_goods_update(self, act_prize):
        """
        @description: 投放商品处理
        """
        act_prize_model = ActPrizeModel()
        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_prize.act_id)
        if act_info.is_throw == 1:
            throw_goods_model = ThrowGoodsModel()
            machine_info_model = MachineInfoModel()
            prize_throw_goods_exist = act_prize_model.get_entity("act_id=%s and goods_id=%s", params=[act_prize.act_id, act_prize.goods_id])
            machine_throw_goods_exist = machine_info_model.get_entity("act_id=%s and goods_id=%s", params=[act_prize.act_id, act_prize.goods_id])
            if not prize_throw_goods_exist and not machine_throw_goods_exist:
                throw_goods_model.update_table("is_throw=0,throw_date=%s,is_sync=0", "act_id=%s and goods_id=%s", params=[self.get_now_datetime(), act_prize.act_id, act_prize.goods_id])


class PrizeReleaseHandler(SevenBaseHandler):
    """
    @description: 上下架奖品
    """
    @filter_check_params("prize_id")
    def get_async(self):
        """
        @description: 上下架奖品
        @param prize_id：奖品id
        @param is_release：0-下架，1-上架
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        prize_id = int(self.get_param("prize_id", "0"))
        is_release = int(self.get_param("is_release", "0"))
        modify_date = self.get_now_datetime()

        if prize_id <= 0:
            return self.reponse_json_error_params()

        ActPrizeModel().update_table("is_release=%s,modify_date=%s", "id=%s", [is_release, modify_date, prize_id])

        self.reponse_json_success()


class PrizeHandler(TopBaseHandler):
    """
    @description: 奖品保存
    """
    @filter_check_params("machine_id,prize_name")
    def post_async(self):
        """
        @description: 奖品保存
        @param prize_id：奖品id
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", "0"))
        prize_id = int(self.get_param("prize_id", "0"))
        machine_id = int(self.get_param("machine_id", "0"))
        prize_type = int(self.get_param("prize_type", "0"))
        tag_id = int(self.get_param("tag_id", "0"))
        sort_index = int(self.get_param("sort_index", "0"))
        prize_pic = self.get_param("prize_pic")
        prize_name = self.get_param("prize_name")
        prize_price = self.get_param("prize_price")
        surplus = int(self.get_param("surplus", "0"))
        is_surplus = int(self.get_param("is_surplus", "0"))
        probability = int(self.get_param("probability", "0"))
        prize_limit = int(self.get_param("prize_limit", "0"))
        prize_detail = self.get_param("prize_detail")
        is_release = int(self.get_param("is_release", "0"))
        is_sku = int(self.get_param("is_sku", "0"))
        goods_id = int(self.get_param("goods_id", "0"))
        force_count = int(self.get_param("force_count", "0"))
        goods_code = self.get_param("goods_code")
        goods_code_list = self.get_param("goods_code_list")
        lottery_type = self.get_param("lottery_type", "1")
        app_id = self.get_param("app_id", "")
        owner_open_id = ""

        if act_id <= 0 or machine_id <= 0:
            return self.reponse_json_error_params()

        act_prize_model = ActPrizeModel()
        act_prize = None
        if prize_id > 0:
            act_prize = act_prize_model.get_entity_by_id(prize_id)

        old_act_prize = {}
        if not act_prize:
            act_prize = ActPrize()
        else:
            old_act_prize = act_prize

        act_prize.act_id = act_id
        act_prize.app_id = app_id
        act_prize.owner_open_id = owner_open_id
        act_prize.machine_id = machine_id
        act_prize.prize_type = prize_type
        act_prize.tag_id = tag_id
        act_prize.sort_index = sort_index
        act_prize.prize_pic = prize_pic
        act_prize.prize_name = prize_name
        act_prize.prize_price = prize_price
        act_prize.surplus = surplus
        act_prize.is_surplus = is_surplus
        act_prize.probability = probability
        act_prize.prize_limit = prize_limit
        act_prize.prize_detail = prize_detail if prize_detail != "" else json.dumps([])
        act_prize.modify_date = self.get_now_datetime()
        act_prize.is_release = is_release
        act_prize.is_sku = is_sku
        act_prize.goods_id = goods_id
        act_prize.goods_code = goods_code
        act_prize.goods_code_list = goods_code_list
        act_prize.force_count = force_count
        act_prize.lottery_type = lottery_type

        if prize_id > 0:
            self.create_operation_log(OperationType.update.value, act_prize.__str__(), "PrizeHandler", old_act_prize, act_prize)
            act_prize_model.update_entity(act_prize)
        else:
            act_prize.create_date = act_prize.modify_date

            if goods_id > 0:
                resp = self.items_seller_list_get_request(str(goods_id), self.get_taobao_param().access_token)
                act_prize.sku_detail = str(resp)

            act_prize.id = act_prize_model.add_entity(act_prize)
            self.create_operation_log(OperationType.add.value, act_prize.__str__(), "PrizeHandler", None, act_prize)

        # 投放商品处理
        self.throw_goods_add(prize_id, act_prize, old_act_prize)

        self.reponse_json_success(act_prize.id)

    def throw_goods_add(self, prize_id, act_prize, old_act_prize):
        """
        @description: 投放商品处理
        """
        act_prize_model = ActPrizeModel()
        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_prize.act_id)
        if act_info.is_throw == 1:
            throw_goods_model = ThrowGoodsModel()
            if prize_id > 0:
                # 商品ID与之前不同的话，改变原该投放商品的状态，并添加新商品ID
                if act_prize.goods_id != old_act_prize.goods_id:
                    machine_info_model = MachineInfoModel()
                    prize_throw_goods_exist = act_prize_model.get_entity("act_id=%s and goods_id=%s", params=[act_prize.act_id, old_act_prize.goods_id])
                    machine_throw_goods_exist = machine_info_model.get_entity("act_id=%s and goods_id=%s", params=[act_prize.act_id, old_act_prize.goods_id])
                    if not prize_throw_goods_exist and not machine_throw_goods_exist:
                        throw_goods_model.update_table("is_throw=0,throw_date=%s,is_sync=0", "act_id=%s and goods_id=%s", params=[self.get_now_datetime(), old_act_prize.act_id, old_act_prize.goods_id])

                    throw_goods = throw_goods_model.get_entity("act_id=%s and goods_id=%s", params=[act_prize.act_id, act_prize.goods_id])
                    if not throw_goods:
                        throw_goods = ThrowGoods()
                        throw_goods.app_id = act_prize.app_id
                        throw_goods.act_id = act_prize.act_id
                        throw_goods.goods_id = act_prize.goods_id
                        throw_goods.is_throw = 0
                        throw_goods.is_sync = 0
                        throw_goods_model.add_entity(throw_goods)
            else:
                throw_goods = throw_goods_model.get_entity("act_id=%s and goods_id=%s", params=[act_prize.act_id, act_prize.goods_id])
                if not throw_goods:
                    throw_goods = ThrowGoods()
                    throw_goods.app_id = act_prize.app_id
                    throw_goods.act_id = act_prize.act_id
                    throw_goods.goods_id = act_prize.goods_id
                    throw_goods.is_throw = 0
                    throw_goods.is_sync = 0
                    throw_goods_model.add_entity(throw_goods)