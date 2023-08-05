# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-05-26 17:51:04
@LastEditTime: 2020-08-20 17:11:25
@LastEditors: HuangJingCan
@Description: 抽奖
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.coin.coin_order_model import *
from seven_cloudapp.models.behavior_model import *

import random


class Lottery2Handler(SevenBaseHandler):
    """
    @description: 
    @param {type} 
    @return: 抽奖
    @last_editors: CaiYouBin
    """
    def get_async(self):
        open_id = self.get_taobao_param().open_id
        app_id = self.get_taobao_param().source_app_id

        machine_id = int(self.get_param("machine_id"))
        login_token = self.get_param("login_token")
        act_id = int(self.get_param("act_id"))

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_mang_he"))
        user_info_model = UserInfoModel(db_transaction=db_transaction)
        machine_value_model = MachineValueModel(db_transaction=db_transaction)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction)
        act_prize_model = ActPrizeModel(db_transaction=db_transaction)
        coin_order_model = CoinOrderModel(db_transaction=db_transaction)

        user_info = user_info_model.get_entity("open_id=%s and app_id=%s and act_id=%s", params=[open_id, app_id, act_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state != 0:
            return self.reponse_json_error("UserState", "对不起，你是黑名单用户,无法拆盒子")
        if user_info.login_token != login_token:
            return self.reponse_json_error("ErrorToken", "对不起，已在另一台设备登录,当前无法抽盲盒")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s and is_release=1", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        now_date = self.get_now_datetime()
        if TimeHelper.format_time_to_datetime(now_date) < TimeHelper.format_time_to_datetime(act_info.start_date):
            return self.reponse_json_error("NoAct", "活动将在" + act_info.start_date + "开启")
        if TimeHelper.format_time_to_datetime(now_date) > TimeHelper.format_time_to_datetime(act_info.end_date):
            return self.reponse_json_error("NoAct", "活动已结束")

        machine_info_model = MachineInfoModel()
        machine_info = machine_info_model.get_entity("id=%s and is_release=1", params=machine_id)
        if not machine_info:
            return self.reponse_json_error("NoMachine", "对不起，盒子不存在")

        prize_field = "id,act_id,award_id,app_id,owner_open_id,machine_id,prize_name,prize_title,prize_pic,prize_detail,goods_id,goods_code,goods_code_list,prize_type,prize_price,probability,surplus,prize_limit,is_surplus,prize_total,tag_id,is_sku,sort_index,is_release"
        act_prize_list = act_prize_model.get_dict_list("machine_id=%s and is_release=1 and surplus>0", field=prize_field, params=machine_id)
        if len(act_prize_list) == 0:
            return self.reponse_json_error("NoMachine", "对不起，该盒子奖品已无库存，暂时无法拆盒子")

        machine_value = machine_value_model.get_entity("machine_id=%s and open_id=%s and act_id=%s", params=[machine_id, open_id, act_id])
        if not machine_value or machine_value.surplus_value <= 0:
            return self.reponse_json_error("NoLotteryCount", "对不起，%s次数不足" % machine_info.machine_name)

        prize_roster_list = prize_roster_model.get_list("open_id=%s and machine_id=%s", params=[open_id, machine_id])

        #中奖限制
        cur_prize_info_list = []
        for act_prize in act_prize_list:
            if act_prize["prize_limit"] > 0:
                mat_prize_list = [i for i in prize_roster_list if i.prize_id == act_prize["id"]]
                if len(mat_prize_list) < act_prize["prize_limit"]:
                    cur_prize_info_list.append(act_prize)
            else:
                cur_prize_info_list.append(act_prize)

        if len(cur_prize_info_list) <= 0:
            return self.reponse_json_error('Error', '抱歉，您在本盒子获得的奖品已达到上限，无法继续拆盒子')

        #抽奖
        try:
            db_transaction.begin_transaction()

            result_prize = self.start_lottery(cur_prize_info_list)

            #扣除用户次数
            machine_value.open_value += 1
            machine_value.surplus_value -= 1
            machine_value.modify_date = self.get_now_datetime()
            machine_value_model.update_entity(machine_value)

            #录入用户奖品
            prize_roster = PrizeRoster()
            prize_roster.app_id = app_id
            prize_roster.act_id = act_id
            prize_roster.open_id = open_id
            prize_roster.machine_id = machine_id
            prize_roster.machine_name = machine_info.machine_name
            prize_roster.machine_price = machine_info.machine_price
            prize_roster.prize_id = result_prize["id"]
            prize_roster.prize_name = result_prize["prize_name"]
            prize_roster.prize_price = result_prize["prize_price"]
            prize_roster.prize_pic = result_prize["prize_pic"]
            prize_roster.prize_detail = result_prize["prize_detail"]
            prize_roster.tag_id = result_prize["tag_id"]
            prize_roster.user_nick = user_info.user_nick
            prize_roster.is_order = 0
            prize_roster.goods_id = result_prize["goods_id"]
            prize_roster.is_sku = result_prize["is_sku"]
            prize_roster.goods_code = result_prize["goods_code"]
            prize_roster.goods_code_list = result_prize["goods_code_list"]
            prize_roster.create_date = self.get_now_datetime()
            # prize_roster_model.add_entity(prize_roster)

            #添加商家对帐记录
            coin_order = None
            coin_order_set = coin_order_model.get_entity("surplus_count>0 and open_id=%s and act_id=%s and machine_id=%s and pay_order_id=0", "id asc", params=[open_id, act_id, machine_id])

            if coin_order_set:
                coin_order_set.surplus_count = coin_order_set.surplus_count - 1
                coin_order = coin_order_set
            else:
                coin_order_pay = coin_order_model.get_entity("surplus_count>0 and open_id=%s and act_id=%s and machine_id=%s and pay_order_id>0", "id asc", params=[open_id, act_id, machine_id])
                if coin_order_pay:
                    coin_order_pay.surplus_count = coin_order_pay.surplus_count - 1
                    coin_order = coin_order_pay

            if coin_order != None:
                coin_order_model.update_entity(coin_order)
                prize_roster.order_no = coin_order.pay_order_no
                if coin_order.pay_order_no != "":
                    prize_roster.frequency_source = 0
                else:
                    prize_roster.frequency_source = 1
            prize_roster_model.add_entity(prize_roster)

            #同步机台奖品库存
            act_prize_model.update_table("surplus=surplus-1,hand_out=hand_out+1", "id=%s", result_prize["id"])

            BehaviorModel().report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'LotteryCount', 1)
            BehaviorModel().report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'LotteryerCount', 1)

            BehaviorModel().report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'openUserCount_' + str(machine_info.id), 1)
            BehaviorModel().report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'openCount_' + str(machine_info.id), 1)

            db_transaction.commit_transaction()
            result_prize_list = [result_prize]

            return self.reponse_json_success(result_prize_list)

        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_error.error(str(ex) + "【拆盒】")

    def start_lottery(self, prize_list):
        """
        @description: 抽奖算法
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        init_value = 0
        probability_list = []
        for prize in prize_list:
            current_prize = prize
            current_prize["start_probability"] = init_value
            current_prize["end_probability"] = init_value + prize["probability"]
            probability_list.append(current_prize)
            init_value = init_value + prize["probability"]

        prize_index = random.randint(0, init_value)

        for prize in probability_list:
            if (prize["start_probability"] <= prize_index and prize_index < prize["end_probability"]):
                return prize


class LotteryHandler(SevenBaseHandler):
    """
    @description: 待测试
    @param {type} 
    @return: 抽奖
    @last_editors: CaiYouBin
    """
    def get_async(self):
        open_id = self.get_taobao_param().open_id
        app_id = self.get_taobao_param().source_app_id

        machine_id = int(self.get_param("machine_id"))
        login_token = self.get_param("login_token")
        act_id = int(self.get_param("act_id"))

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_mang_he"))
        user_info_model = UserInfoModel(db_transaction=db_transaction)
        machine_value_model = MachineValueModel(db_transaction=db_transaction)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction)
        act_prize_model = ActPrizeModel(db_transaction=db_transaction)
        coin_order_model = CoinOrderModel(db_transaction=db_transaction)

        user_info = user_info_model.get_entity("open_id=%s and app_id=%s and act_id=%s", params=[open_id, app_id, act_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state != 0:
            return self.reponse_json_error("UserState", "对不起，你是黑名单用户,无法拆盒子")
        if user_info.login_token != login_token:
            return self.reponse_json_error("ErrorToken", "对不起，已在另一台设备登录,当前无法抽盲盒")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s and is_release=1", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        now_date = self.get_now_datetime()
        if TimeHelper.format_time_to_datetime(now_date) < TimeHelper.format_time_to_datetime(act_info.start_date):
            return self.reponse_json_error("NoAct", "活动将在" + act_info.start_date + "开启")
        if TimeHelper.format_time_to_datetime(now_date) > TimeHelper.format_time_to_datetime(act_info.end_date):
            return self.reponse_json_error("NoAct", "活动已结束")

        machine_info_model = MachineInfoModel()
        machine_info = machine_info_model.get_entity("id=%s and is_release=1", params=machine_id)
        if not machine_info:
            return self.reponse_json_error("NoMachine", "对不起，盒子不存在")

        identifier = self.acquire_lock("machine_id_" + str(machine_id) + "_lottery")

        if isinstance(identifier, bool):
            return self.reponse_json_error("UserLimit", "当前人数过多,请稍后再来")

        try:
            db_transaction.begin_transaction()

            prize_field = "id,act_id,award_id,app_id,owner_open_id,machine_id,prize_name,prize_title,prize_pic,prize_detail,goods_id,goods_code,goods_code_list,prize_type,prize_price,probability,surplus,prize_limit,is_surplus,prize_total,tag_id,is_sku,sort_index,is_release,force_count"
            act_prize_list = act_prize_model.get_dict_list("machine_id=%s and is_release=1 and surplus>0", field=prize_field, params=machine_id)
            if len(act_prize_list) == 0:
                self.release_lock("machine_id_" + str(machine_id) + "_lottery", identifier)
                return self.reponse_json_error("NoMachine", "对不起，该盒子奖品已无库存，暂时无法拆盒子")

            machine_value = machine_value_model.get_entity("machine_id=%s and open_id=%s and act_id=%s", params=[machine_id, open_id, act_id])
            if not machine_value or machine_value.surplus_value <= 0:
                self.release_lock("machine_id_" + str(machine_id) + "_lottery", identifier)
                return self.reponse_json_error("NoLotteryCount", "对不起，%s次数不足" % machine_info.machine_name)

            prize_roster_list = prize_roster_model.get_list("open_id=%s and machine_id=%s", params=[open_id, machine_id])

            #中奖限制
            cur_prize_info_list = []
            for act_prize in act_prize_list:
                if act_prize["prize_limit"] > 0:
                    mat_prize_list = [i for i in prize_roster_list if i.prize_id == act_prize["id"]]
                    if len(mat_prize_list) < act_prize["prize_limit"]:
                        cur_prize_info_list.append(act_prize)
                else:
                    cur_prize_info_list.append(act_prize)

            if len(cur_prize_info_list) <= 0:
                self.release_lock("machine_id_" + str(machine_id) + "_lottery", identifier)
                return self.reponse_json_error('Error', '抱歉，您在本盒子获得的奖品已达到上限，无法继续拆盒子')

            #强制命中算法
            must_prize_list = []
            prize_roster_total = prize_roster_model.get_total("machine_id=%s", params=machine_id)

            cur_prize_info_list2 = []
            for cur_prize_info in cur_prize_info_list:
                if cur_prize_info["force_count"] > 0:
                    page_total = int(prize_roster_total / cur_prize_info["force_count"])
                    prize_roster_after_list = prize_roster_model.get_dict_list("machine_id=%s", "", "id asc", str(page_total * cur_prize_info["force_count"]) + "," + str((page_total * cur_prize_info["force_count"]) + cur_prize_info["force_count"]), params=machine_id)

                    is_exist = [prize_roster_after for prize_roster_after in prize_roster_after_list if prize_roster_after["prize_id"] == cur_prize_info["id"]]
                    if len(is_exist) == 0:
                        if (prize_roster_total + 1) % cur_prize_info["force_count"] == 0:
                            must_prize_list.append(cur_prize_info)
                        else:
                            cur_prize_info_list2.append(cur_prize_info)
                else:
                    cur_prize_info_list2.append(cur_prize_info)
            if len(must_prize_list) > 0:
                cur_prize_info_list = must_prize_list
            else:
                cur_prize_info_list = cur_prize_info_list2

            #抽奖
            result_prize = self.start_lottery(cur_prize_info_list)

            #扣除用户次数
            machine_value.open_value += 1
            machine_value.surplus_value -= 1
            machine_value.modify_date = self.get_now_datetime()
            machine_value_model.update_entity(machine_value)

            #录入用户奖品
            prize_roster = PrizeRoster()
            prize_roster.app_id = app_id
            prize_roster.act_id = act_id
            prize_roster.open_id = open_id
            prize_roster.machine_id = machine_id
            prize_roster.machine_name = machine_info.machine_name
            prize_roster.machine_price = machine_info.machine_price
            prize_roster.prize_id = result_prize["id"]
            prize_roster.prize_name = result_prize["prize_name"]
            prize_roster.prize_price = result_prize["prize_price"]
            prize_roster.prize_pic = result_prize["prize_pic"]
            prize_roster.prize_detail = result_prize["prize_detail"]
            prize_roster.tag_id = result_prize["tag_id"]
            prize_roster.user_nick = user_info.user_nick
            prize_roster.is_order = 0
            prize_roster.goods_id = result_prize["goods_id"]
            prize_roster.is_sku = result_prize["is_sku"]
            prize_roster.goods_code = result_prize["goods_code"]
            prize_roster.goods_code_list = result_prize["goods_code_list"]
            prize_roster.create_date = self.get_now_datetime()
            # prize_roster_model.add_entity(prize_roster)

            #添加商家对帐记录
            coin_order = None
            coin_order_set = coin_order_model.get_entity("surplus_count>0 and open_id=%s and act_id=%s and machine_id=%s and pay_order_id=0", "id asc", params=[open_id, act_id, machine_id])

            if coin_order_set:
                coin_order_set.surplus_count = coin_order_set.surplus_count - 1
                coin_order = coin_order_set
            else:
                coin_order_pay = coin_order_model.get_entity("surplus_count>0 and open_id=%s and act_id=%s and machine_id=%s and pay_order_id>0", "id asc", params=[open_id, act_id, machine_id])
                if coin_order_pay:
                    coin_order_pay.surplus_count = coin_order_pay.surplus_count - 1
                    coin_order = coin_order_pay

            if coin_order != None:
                coin_order_model.update_entity(coin_order)
                prize_roster.order_no = coin_order.pay_order_no
                if coin_order.pay_order_no != "":
                    prize_roster.frequency_source = 0
                else:
                    prize_roster.frequency_source = 1
            prize_roster_model.add_entity(prize_roster)

            #同步机台奖品库存
            act_prize_model.update_table("surplus=surplus-1,hand_out=hand_out+1", "id=%s", result_prize["id"])

            BehaviorModel().report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'LotteryCount', 1)
            BehaviorModel().report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'LotteryerCount', 1)

            BehaviorModel().report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'openUserCount_' + str(machine_info.id), 1)
            BehaviorModel().report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'openCount_' + str(machine_info.id), 1)

            db_transaction.commit_transaction()
            result_prize_list = [result_prize]

            self.release_lock("machine_id_" + str(machine_id) + "_lottery", identifier)
            return self.reponse_json_success(result_prize_list)

        except Exception as ex:
            self.logger_error.error(str(ex) + "【拆盒】")
            self.release_lock("machine_id_" + str(machine_id) + "_lottery", identifier)
            db_transaction.rollback_transaction()

    def start_lottery(self, prize_list):
        """
        @description: 抽奖算法
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        init_value = 0
        probability_list = []
        for prize in prize_list:
            current_prize = prize
            current_prize["start_probability"] = init_value
            current_prize["end_probability"] = init_value + prize["probability"]
            probability_list.append(current_prize)
            init_value = init_value + prize["probability"]

        prize_index = random.randint(0, init_value - 1)

        for prize in probability_list:
            if (prize["start_probability"] <= prize_index and prize_index < prize["end_probability"]):
                return prize
