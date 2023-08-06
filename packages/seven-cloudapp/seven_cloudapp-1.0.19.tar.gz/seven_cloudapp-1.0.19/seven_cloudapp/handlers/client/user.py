# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-19 11:33:16
@LastEditTime: 2020-09-07 17:39:57
@LastEditors: HuangJingCan
@Description: 用户处理
"""
import decimal
from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.pay.pay_order_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.prize.prize_order_model import *
from seven_cloudapp.models.db_models.behavior.behavior_orm_model import *
from seven_cloudapp.models.db_models.behavior.behavior_log_model import *
from seven_cloudapp.models.db_models.behavior.behavior_report_model import *
from seven_cloudapp.models.db_models.coin.coin_order_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.behavior_model import *

from seven_cloudapp.models.seven_model import PageInfo

from seven_cloudapp.libs.customize.seven import *


class LoginHandler(SevenBaseHandler):
    """
    @description: 登录处理
    @param {type} 
    @return: 
    @last_editors: HuangJingCan
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 登录日志入库
        @param open_id：用户唯一标识
        @return: 登录
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        app_id = self.get_taobao_param().source_app_id

        avatar = self.get_param("avatar")
        is_auth = int(self.get_param("is_auth", "0"))
        owner_open_id = self.get_param("owner_open_id")
        login_token = self.get_param("login_token")
        signin = self.get_param("signin")
        act_id = int(self.get_param("act_id", "0"))

        # request_params = str(self.request_params)

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("app_id=%s and act_id=%s and open_id=%s", params=[app_id, act_id, open_id])

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        machine_info_model = MachineInfoModel()
        machine_info_list = machine_info_model.get_list("app_id=%s and act_id=%s", params=[app_id, act_id])
        if not machine_info_list:
            return self.reponse_json_error("NoMachine", "对不起，盲盒不存在")

        is_add = False
        if not user_info:
            is_add = True
        if is_add:
            user_info = self.get_default_user(act_id)

            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.id = user_info_model.add_entity(user_info)
        else:
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.is_new = 0
            user_info_model.update_entity(user_info)

        machine_value_model = MachineValueModel()
        machine_value_list = machine_value_model.get_dict_list("open_id=%s", params=open_id)
        user_info_dict = user_info.__dict__
        user_info_dict["machine_value_list"] = machine_value_list

        behavior_model = BehaviorModel()
        # 访问次数
        behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitCountEveryDay', 1)
        # 访问人数
        behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDay', 1)
        if user_info.is_new == 1:
            # 新增用户数
            behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDayIncrease', 1)
        self.reponse_json_success(user_info_dict)


class UserHandler(SevenBaseHandler):
    """
    @description: 更新用户信息
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    @filter_check_params("act_id")
    def get_async(self):
        try:
            user_nick = self.get_taobao_param().user_nick
            avatar = self.get_param("avatar")
            act_id = self.get_param("act_id")
            open_id = self.get_taobao_param().open_id
            source_app_id = self.get_taobao_param().source_app_id

            user_info_model = UserInfoModel()
            user_info = user_info_model.get_entity("open_id=%s and app_id=%s and act_id=%s", params=[open_id, source_app_id, act_id])
            if not user_info:
                return self.reponse_json_error("NoUser", "对不起，用户不存在")
            user_info.user_nick = user_nick
            user_info.avatar = avatar
            user_info.is_auth = 1
            user_info.modify_date = self.get_now_datetime()
            user_info_model.update_entity(user_info)
            self.reponse_json_success('更新成功')
        except Exception as ex:
            self.reponse_json_error('Error', '更新失败')


class SyncPayOrderHandler(TopBaseHandler):
    """
    @description: 用户支付订单提交
    @param {type} 
    @return: 
    @last_editors: HuangJingCan
    """
    @filter_check_params()
    def get_async(self):
        act_id = self.get_param("act_id")
        open_id = self.get_taobao_param().open_id
        app_id = self.get_taobao_param().source_app_id

        user_info_model = UserInfoModel()
        access_token = ""
        app_info = AppInfoModel().get_entity("app_id=%s", params=self.get_taobao_param().source_app_id)
        if app_info:
            access_token = app_info.access_token
        user_info = user_info_model.get_entity("act_id=%s and open_id=%s and app_id=%s", params=[act_id, open_id, app_id])
        if not user_info:
            return self.reponse_json_error('NoUser', '对不起，用户不存在')
        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity('id=%s and app_id=%s', params=[act_id, app_id])
        if not act_info:
            return self.reponse_json_error('NoAct', '对不起，活动不存在')
        # 获取订单
        order_data = []
        if self.get_is_test() == True:
            order_data = json.loads(self.test_order())
        else:
            order_data = self.get_taobao_order(open_id, access_token)
            # self.logger_info.info(str(order_data) + "【订单列表】")

        #获取所有盲盒配置
        machine_info_model = MachineInfoModel()
        machine_config_list = machine_info_model.get_list("app_id=%s and act_id=%s", params=[app_id, act_id])

        pay_order_model = PayOrderModel()
        pay_order_list = pay_order_model.get_list("app_id=%s and open_id=%s and act_id=%s", params=[app_id, open_id, act_id])

        pay_order_id_list = []
        for item in pay_order_list:
            pay_order_id_list.append(item.order_no)

        buy_goods_id_list = []
        for item in machine_config_list:
            buy_goods_id_list.append(item.goods_id)

        #所有订单(排除交易结束订单)
        all_sub_order_list = []
        #所有相关商品订单
        all_goods_order_list = []

        #过滤掉不奖励的数据和跟活动无关的订单
        for item in order_data:
            for order in item["orders"]["order"]:
                if str(order["num_iid"]) in buy_goods_id_list:
                    if order["status"] in self.rewards_status():
                        order["pay_time"] = item["pay_time"]
                        order["tid"] = item["tid"]
                        all_sub_order_list.append(order)
                    if "pay_time" in item:
                        order["tid"] = item["tid"]
                        order["pay_time"] = item["pay_time"]
                        all_goods_order_list.append(order)

        add_lottery_count = False
        total_pay_num = 0
        total_pay_prize = 0
        total_pay_order_num = 0
        user_info_dict = {}

        for order in all_sub_order_list:
            #判断是否已经加过奖励
            if order["oid"] not in pay_order_id_list:

                pay_order = PayOrder()
                pay_order.app_id = app_id
                pay_order.act_id = act_id
                pay_order.open_id = open_id
                pay_order.owner_open_id = act_info.owner_open_id
                pay_order.user_nick = user_info.user_nick
                pay_order.main_order_no = order['tid']
                pay_order.order_no = order['oid']
                pay_order.goods_code = order['num_iid']
                pay_order.goods_name = order['title']
                if "sku_id" in order.keys():
                    pay_order.sku_id = order['sku_id']
                pay_order.buy_num = order['num']
                pay_order.pay_price = order['payment']
                pay_order.order_status = order['status']
                pay_order.create_date = self.get_now_datetime()
                pay_order.pay_date = order['pay_time']

                now_machine_config = {}
                for machine_config in machine_config_list:
                    if (machine_config.goods_modify_date == '1900-01-01 00:00:00' or TimeHelper.format_time_to_datetime(machine_config.goods_modify_date) < TimeHelper.format_time_to_datetime(order["pay_time"])) and machine_config.goods_id == str(order["num_iid"]):
                        now_machine_config = machine_config
                        continue

                if now_machine_config:
                    if "sku_id" in order.keys():
                        pay_order.sku_name = self.get_sku_name(int(order['num_iid']), int(order['sku_id']), access_token)
                    pay_order_id = pay_order_model.add_entity(pay_order)
                    #获得次数
                    prize_machine_count = int(order["num"])

                    machine_value_model = MachineValueModel()
                    machine_value = machine_value_model.get_entity("act_id=%s and machine_id=%s and open_id=%s", params=[act_id, now_machine_config.id, open_id])
                    if not machine_value:
                        machine_value = MachineValue()
                        machine_value.act_id = act_id
                        machine_value.app_id = app_id
                        machine_value.open_id = open_id
                        machine_value.machine_id = now_machine_config.id
                        machine_value.surplus_value = prize_machine_count
                        machine_value.create_date = self.get_now_datetime()
                        machine_value.modify_date = self.get_now_datetime()
                        machine_value_model.add_entity(machine_value)
                    else:
                        machine_value.surplus_value += prize_machine_count
                        machine_value.modify_date = self.get_now_datetime()
                        machine_value_model.update_entity(machine_value)

                    user_info.pay_num += prize_machine_count
                    user_info.pay_price = str(decimal.Decimal(user_info.pay_price) + decimal.Decimal(order["payment"]))
                    user_info_model.update_entity(user_info)

                    machine_value_list_dict = machine_value_model.get_dict_list("act_id=%s and open_id=%s", params=[act_id, open_id])

                    total_pay_num += 1
                    total_pay_prize = str(decimal.Decimal(total_pay_prize) + decimal.Decimal(order["payment"]))
                    total_pay_order_num += int(order["num"])
                    add_lottery_count = True
                    user_info_dict = user_info.__dict__
                    user_info_dict["machine_value_list"] = machine_value_list_dict

                    #添加记录
                    coin_order_model = CoinOrderModel()
                    coin_order = CoinOrder()
                    coin_order.open_id = open_id
                    coin_order.app_id = app_id
                    coin_order.act_id = act_id
                    coin_order.machine_id = now_machine_config.id
                    coin_order.reward_type = 0
                    coin_order.goods_name = pay_order.goods_name
                    coin_order.goods_price = pay_order.pay_price
                    coin_order.sku = pay_order.sku_id
                    coin_order.nick_name = pay_order.user_nick
                    coin_order.main_pay_order_no = pay_order.main_order_no
                    coin_order.pay_order_no = pay_order.order_no
                    coin_order.pay_order_id = pay_order_id
                    coin_order.buy_count = prize_machine_count
                    coin_order.surplus_count = prize_machine_count
                    coin_order.pay_date = pay_order.pay_date
                    coin_order.create_date = self.get_now_datetime()
                    coin_order.modify_date = self.get_now_datetime()
                    coin_order_model.add_entity(coin_order)
                #结束

        if user_info.user_state == 0 and act_info.is_black == 1 and act_info.refund_count > 0:
            #退款的订单  子订单存在退款 记录一次
            # refund_order_data = [i for i in all_goods_order_list if [j for j in i if j["refund_status"] not in self.refund_status()]]
            refund_order_data = [i for i in all_goods_order_list if i["refund_status"] not in self.refund_status()]
            #如果不是黑用户 并且存在退款时间 代表黑用户解禁
            if user_info.relieve_date != '1900-01-01 00:00:00':
                refund_order_data = [i for i in refund_order_data if TimeHelper.format_time_to_datetime(i['pay_time']) > TimeHelper.format_time_to_datetime(user_info.relieve_date)]
            #超过变成黑用户
            if len(refund_order_data) >= act_info.refund_count:
                user_info_model.update_table("user_state=1", "id=%s", user_info.id)
                user_info_dict["user_state"] = 1

        result = {}
        if add_lottery_count == True:
            result["user_info"] = user_info_dict
            result["total_pay_order_num"] = total_pay_order_num
            result["total_pay_num"] = total_pay_num
            result["total_pay_prize"] = total_pay_prize

            behavior_model = BehaviorModel()
            behavior_model.report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'PayMoneyCount', decimal.Decimal(total_pay_prize))
            behavior_model.report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'PayerCount', 1)
            behavior_model.report_behavior(app_id, act_id, open_id, act_info.owner_open_id, 'PayCount', total_pay_num)

            self.reponse_json_success(result)
        else:
            self.reponse_json_success()


class UserPrizeListHandler(SevenBaseHandler):
    """
    @description: 获取用户奖品列表
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id"))
        status = int(self.get_param("status", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        prize_roster_model = PrizeRosterModel()
        if status == 0:
            condition = "open_id=%s and act_id=%s and prize_order_id=0"
        else:
            condition = "open_id=%s and act_id=%s and prize_order_id>0"

        page_list, total = prize_roster_model.get_dict_page_list("*", page_index, page_size, condition, "", "create_date desc", [open_id, act_id])

        page_info = PageInfo(page_index, page_size, total, page_list)

        self.reponse_json_success(page_info)


class SubmitPrizeOrder(SevenBaseHandler):
    """
    @description: 奖品订单提交
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id"))
        login_token = self.get_param("login_token")
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        province = self.get_param("province")
        city = self.get_param("city")
        county = self.get_param("county")
        street = self.get_param("street")
        address = self.get_param("address")

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("open_id=%s and app_id=%s and act_id=%s", params=[open_id, app_id, act_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.reponse_json_error("UserBlock", "对不起，你是黑名单用户,无法提交订单")
        if user_info.login_token != login_token:
            return self.reponse_json_error("ErrorLoginToken", "对不起，帐号已在另一台设备登录,当前无法提交订单")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s and is_del=0 and is_release=1", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        prize_roster_model = PrizeRosterModel()
        prize_roster_count = prize_roster_model.get_total("act_id=%s and open_id=%s and prize_order_id=0", params=[act_id, open_id])
        if prize_roster_count == 0:
            return self.reponse_json_error("NoNeedSubmitPrize", "当前没有未提交订单的奖品")

        prize_order_model = PrizeOrderModel()
        prize_order = PrizeOrder()
        prize_order.app_id = app_id
        prize_order.open_id = open_id
        prize_order.act_id = act_id
        prize_order.user_nick = user_info.user_nick
        prize_order.real_name = real_name
        prize_order.telephone = telephone
        prize_order.province = province
        prize_order.city = city
        prize_order.county = county
        prize_order.street = street
        prize_order.adress = address
        prize_order.create_date = self.get_now_datetime()
        prize_order.modify_date = self.get_now_datetime()
        prize_order.order_no = self.create_order_id()

        prize_order.id = prize_order_model.add_entity(prize_order)

        prize_roster_model.update_table("prize_order_id=%s,prize_order_no=%s", "act_id=%s and open_id=%s and prize_order_id=0", params=[prize_order.id, prize_order.order_no, act_id, open_id])

        self.reponse_json_success()


class RosterNoticeHandler(SevenBaseHandler):
    """
    @description: 中奖通告
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):
        act_id = self.get_param("act_id")

        prize_roster_model = PrizeRosterModel()
        prize_roster_field = "id,app_id,act_id,open_id,machine_id,machine_name,machine_price,prize_id,prize_name,prize_price,prize_pic,prize_detail,tag_id,award_id,award_name,user_nick,prize_code,order_status,is_sku,prize_order_id,prize_order_no,sku_id,properties_name,goods_id,goods_code,goods_code_list,order_no,frequency_source,create_date"
        prize_roster_list_dict = prize_roster_model.get_dict_list("act_id=%s", order_by="create_date desc", field=prize_roster_field, limit="20", params=act_id)

        self.reponse_json_success(prize_roster_list_dict)


class PrizeRosterNoSubmitNum(SevenBaseHandler):
    """
    @description: 没有提交的用户奖品数
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):

        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id"))

        prize_roster_model = PrizeRosterModel()
        prize_roster_total = prize_roster_model.get_total("act_id=%s and open_id=%s and is_sku=1 and sku_id ='' ", params=[act_id, open_id])

        self.reponse_json_success(prize_roster_total)


class PrizeOrderHandler(SevenBaseHandler):
    """
    @description: 用户订单列表
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id"))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        prize_order_model = PrizeOrderModel()
        prize_roster_model = PrizeRosterModel()
        prize_order_list_dict, total = prize_order_model.get_dict_page_list("*", page_index, page_size, "open_id=%s and act_id=%s ", "", "create_date desc", [open_id, act_id])
        if prize_order_list_dict:
            prize_order_id_list = [i["id"] for i in prize_order_list_dict]
            prize_order_ids = str(prize_order_id_list).strip('[').strip(']')
            prize_roster_field = "id,app_id,act_id,open_id,machine_id,machine_name,machine_price,prize_id,prize_name,prize_price,prize_pic,prize_detail,tag_id,award_id,award_name,user_nick,prize_code,order_status,is_sku,prize_order_id,prize_order_no,sku_id,properties_name,goods_id,goods_code,goods_code_list,order_no,frequency_source,create_date"
            prize_roster_list_dict = prize_roster_model.get_dict_list("prize_order_id in (" + prize_order_ids + ")", field=prize_roster_field)
            for i in range(len(prize_order_list_dict)):
                prize_order_list_dict[i]["prize_order_list"] = [prize_roster for prize_roster in prize_roster_list_dict if prize_order_list_dict[i]["id"] == prize_roster["prize_order_id"]]

        page_info = PageInfo(page_index, page_size, total, prize_order_list_dict)

        self.reponse_json_success(page_info)