# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-29 09:40:42
@LastEditTime: 2020-08-17 10:41:01
@LastEditors: CaiYouBin
@Description: 机台（盒子）
"""

import decimal
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.db_models.machine.machine_value_log_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.behavior.behavior_log_model import *
from seven_cloudapp.models.db_models.behavior.behavior_orm_model import *
from seven_cloudapp.models.db_models.behavior.behavior_report_model import *
from seven_cloudapp.models.db_models.coin.coin_order_model import *
from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.seven_model import PageInfo
from seven_cloudapp.models.enum import *


class MachineHandler(SevenBaseHandler):
    """
    @description: 保存机台
    """
    @filter_check_params("act_id,machine_name")
    def post_async(self):
        """
        @description: 保存机台
        @param machine_id：机台id
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        app_id = self.get_param("app_id")
        machine_id = int(self.get_param("machine_id", "0"))
        act_id = int(self.get_param("act_id", "0"))
        machine_name = self.get_param("machine_name")
        machine_type = int(self.get_param("machine_type", "0"))
        goods_id = self.get_param("goods_id")
        sku_id = self.get_param("sku_id")
        skin_id = int(self.get_param("skin_id", "0"))
        sort_index = int(self.get_param("sort_index", "0"))
        is_release = int(self.get_param("is_release", "0"))
        single_lottery_price = int(self.get_param("single_lottery_price", "0"))
        many_lottery_price = int(self.get_param("many_lottery_price", "0"))
        many_lottery_num = int(self.get_param("many_lottery_num", "0"))
        machine_price = decimal.Decimal(self.get_param("machine_price", "0.00"))
        is_repeat_prize = int(self.get_param("is_repeat_prize", "0"))

        if act_id <= 0:
            return self.reponse_json_error_params()

        machine_info = None
        machine_info_model = MachineInfoModel()
        if machine_id > 0:
            machine_info = machine_info_model.get_entity_by_id(machine_id)

        is_add = False
        if not machine_info:
            is_add = True
            machine_info = MachineInfo()

        old_machine_info = machine_info
        machine_info.act_id = act_id
        machine_info.app_id = app_id
        machine_info.machine_name = machine_name
        machine_info.machine_type = machine_type
        machine_info.goods_id = goods_id
        machine_info.sku_id = sku_id
        machine_info.skin_id = skin_id
        machine_info.sort_index = sort_index
        machine_info.is_release = is_release
        machine_info.single_lottery_price = single_lottery_price
        machine_info.many_lottery_price = many_lottery_price
        machine_info.many_lottery_num = many_lottery_num
        machine_info.machine_price = decimal.Decimal(machine_price)
        machine_info.is_repeat_prize = is_repeat_prize
        machine_info.goods_modify_date = self.get_now_datetime()
        machine_info.modify_date = machine_info.goods_modify_date

        exist_goods_id = machine_info_model.get_entity("goods_id=%s and id<>%s", params=[goods_id, machine_info.id])
        if exist_goods_id:
            return self.reponse_json_error("ExistGoodsID", "对不起，当前商品ID已应用到其他盒子中")

        if is_add:
            machine_info.create_date = machine_info.modify_date
            machine_info.id = machine_info_model.add_entity(machine_info)
            # 记录日志
            self.create_operation_log(OperationType.add.value, machine_info.__str__(), "MachineHandler", None, self.json_dumps(machine_info))
        else:
            machine_info_model.update_entity(machine_info)
            self.create_operation_log(OperationType.update.value, machine_info.__str__(), "MachineHandler", self.json_dumps(old_machine_info), self.json_dumps(machine_info))

        # 增加行为映射数据
        orm_infos = []

        for i in range(0, 2):
            behavior_orm = BehaviorOrm()
            if i == 0:
                behavior_orm.is_repeat = 0
                behavior_orm.key_value = machine_info.machine_name + "拆开次数"
                behavior_orm.key_name = "openCount_" + str(machine_info.id)
            else:
                behavior_orm.is_repeat = 1
                behavior_orm.key_value = machine_info.machine_name + "拆开人数"
                behavior_orm.key_name = "openUserCount_" + str(machine_info.id)
            behavior_orm.orm_type = 1
            behavior_orm.group_name = ""
            behavior_orm.is_common = 0
            behavior_orm.sort_index = 1
            behavior_orm.app_id = app_id
            behavior_orm.act_id = act_id
            behavior_orm.create_date = self.get_now_datetime()
            orm_infos.append(behavior_orm)

        self.save_orm(orm_infos, act_id)

        self.reponse_json_success(machine_info.id)

    def save_orm(self, orm_infos, act_id):
        """
        @description: 保存Orm
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        delete_orm_ids = []
        behavior_orm_model = BehaviorOrmModel()
        behavior_orm_list = behavior_orm_model.get_list('act_id=%s', params=act_id)
        for behavior_orm_item in behavior_orm_list:
            if behavior_orm_item.key_name.find(orm_infos[0].key_name) != -1:
                delete_orm_ids.append(str(behavior_orm_item.id))
            if behavior_orm_item.key_name.find(orm_infos[1].key_name) != -1:
                delete_orm_ids.append(str(behavior_orm_item.id))
        if len(delete_orm_ids) > 0:
            delete_orm_id_strs = ','.join(delete_orm_ids)
            behavior_orm_model.del_entity('id in (' + delete_orm_id_strs + ')')
        behavior_orm_model.add_list(orm_infos)


class MachineListHandler(SevenBaseHandler):
    """
    @description: 机台信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取机台列表
        @param act_id：活动id
        @param page_index：页索引
        @param page_size：页大小
        @return: list
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", "0"))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))

        if act_id <= 0:
            return self.reponse_json_error_params()

        page_list, total = MachineInfoModel().get_page_list("*", page_index, page_size, "act_id=%s", "", "sort_index desc", act_id)

        new_list = []
        for page in page_list:
            machine_info = {}
            machine_info["id"] = page.id
            machine_info["sort_index"] = page.sort_index
            machine_info["machine_name"] = page.machine_name
            machine_info["machine_type"] = page.machine_type
            machine_info["machine_price"] = page.machine_price
            machine_info["goods_id"] = page.goods_id
            machine_info["skin_id"] = page.skin_id
            # 可被抽中奖品件数
            prize_count = ActPrizeModel().get_total("machine_id=%s AND probability>0 AND surplus>0 AND is_release=1", params=page.id)
            machine_info["prize_count"] = prize_count
            machine_info["is_release"] = page.is_release

            new_list.append(machine_info)

        page_info = PageInfo(page_index, page_size, total, new_list)

        self.reponse_json_success(page_info)


class MachineDelHandler(SevenBaseHandler):
    """
    @description: 删除机台
    """
    @filter_check_params("machine_id")
    def get_async(self):
        """
        @description: 删除机台
        @param machine_id：机台id
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        machine_id = int(self.get_param("machine_id", "0"))

        if machine_id <= 0:
            return self.reponse_json_error_params()

        ActPrizeModel().del_entity("machine_id=%s", machine_id)

        MachineInfoModel().del_entity("id=%s", machine_id)

        MachineValueModel().del_entity("machine_id=%s", machine_id)

        BehaviorOrmModel().del_entity("key_name='openUserCount_" + str(machine_id) + "' or key_name='openCount_" + str(machine_id) + "'")

        self.create_operation_log(OperationType.delete.value, "machine_info_tb", "MachineHandler", None, machine_id)

        self.reponse_json_success()


class MachineReleaseHandler(SevenBaseHandler):
    """
    @description: 机台上下架
    """
    @filter_check_params("machine_id,is_release")
    def get_async(self):
        """
        @description: 机台上下架
        @param machine_id：机台id
        @param is_release：是否发布（0下架1上架）
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        machine_id = int(self.get_param("machine_id", "0"))
        is_release = int(self.get_param("is_release", "0"))

        if machine_id <= 0:
            return self.reponse_json_error_params()

        MachineInfoModel().update_table("is_release=%s", "id=%s", [is_release, machine_id])

        self.reponse_json_success()


class MachineValueHandler(SevenBaseHandler):
    """
    @description: 设置开盒次数
    """
    @filter_check_params("user_open_id,act_id")
    def post_async(self):
        """
        @description: 设置开盒次数
        @param surplus_value：剩余次数
        @param user_open_id：用户唯一标识x
        @param machine_id：机台id
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        user_open_id = self.get_param("user_open_id")
        set_content_list = self.get_param("set_content_list")
        act_id = int(self.get_param("act_id", "0"))
        app_id = self.get_param("app_id")
        modify_date = self.get_now_datetime()

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("open_id=%s and act_id=%s", params=[user_open_id, act_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，找不到该用户")

        machine_value_model = MachineValueModel()

        if act_id <= 0:
            return self.reponse_json_error_params()

        set_content_list = json.loads(set_content_list)

        for set_content in set_content_list:
            machine_id = set_content["machine_id"]
            surplus_value = set_content["surplus_value"]

            result = False
            old_surplus_value = 0
            dict_surplus_value = machine_value_model.get_dict("open_id=%s AND machine_id=%s", field="surplus_value", params=[user_open_id, machine_id])
            if dict_surplus_value:
                old_surplus_value = dict_surplus_value.get("surplus_value")
                if old_surplus_value != surplus_value:
                    result = machine_value_model.update_table("surplus_value=%s,modify_date=%s", "open_id=%s AND machine_id=%s", [surplus_value, modify_date, user_open_id, machine_id])
            else:
                if surplus_value == 0:
                    result = True
                else:
                    machine_value = MachineValue()
                    machine_value.act_id = act_id
                    machine_value.app_id = app_id
                    machine_value.open_id = user_open_id
                    machine_value.machine_id = machine_id
                    machine_value.open_value = 0
                    machine_value.surplus_value = surplus_value
                    machine_value.modify_date = modify_date
                    machine_value.create_date = modify_date
                    result = machine_value_model.add_entity(machine_value)
                if result > 0:
                    result = True

            if result:
                machine_value_log = MachineValueLog()
                machine_value_log.app_id = app_id
                machine_value_log.act_id = act_id
                machine_value_log.open_id = user_open_id
                machine_value_log.machine_id = machine_id
                machine_value_log.source_type = SourceType.手动配置.value
                machine_value_log.increase_value = surplus_value - old_surplus_value
                machine_value_log.old_surplus_value = old_surplus_value
                machine_value_log.create_date = modify_date
                MachineValueLogModel().add_entity(machine_value_log)

                #添加商家对帐记录
                coin_order_model = CoinOrderModel()
                if (surplus_value - old_surplus_value) > 0:
                    coin_order = CoinOrder()
                    coin_order.open_id = user_open_id
                    coin_order.app_id = app_id
                    coin_order.act_id = act_id
                    coin_order.machine_id = machine_id
                    coin_order.reward_type = 0
                    coin_order.nick_name = user_info.user_nick
                    coin_order.buy_count = surplus_value - old_surplus_value
                    coin_order.surplus_count = surplus_value - old_surplus_value
                    coin_order.create_date = self.get_now_datetime()
                    coin_order.modify_date = self.get_now_datetime()
                    coin_order_model.add_entity(coin_order)
                else:
                    del_count = old_surplus_value - surplus_value
                    update_coin_order_list = []
                    coin_order_set_list = coin_order_model.get_list("surplus_count>0 and open_id=%s and act_id=%s and machine_id=%s and pay_order_id=0", "id asc", params=[user_open_id, act_id, machine_id])

                    if len(coin_order_set_list) > 0:
                        for coin_order in coin_order_set_list:
                            if coin_order.surplus_count > del_count:
                                coin_order.surplus_count = coin_order.surplus_count - del_count
                                del_count = 0
                            else:
                                del_count = del_count - coin_order.surplus_count
                                coin_order.surplus_count = 0
                            update_coin_order_list.append(coin_order)
                            if del_count == 0:
                                break
                    if del_count > 0:
                        coin_order_pay_list = coin_order_model.get_list("surplus_count>0 and open_id=%s and act_id=%s and machine_id=%s and pay_order_id>0", "id asc", params=[user_open_id, act_id, machine_id])
                        if len(coin_order_pay_list) > 0:
                            for coin_order in coin_order_pay_list:
                                if coin_order.surplus_count > del_count:
                                    coin_order.surplus_count = coin_order.surplus_count - del_count
                                    del_count = 0
                                else:
                                    del_count = del_count - coin_order.surplus_count
                                    coin_order.surplus_count = 0
                                update_coin_order_list.append(coin_order)
                                if del_count == 0:
                                    break
                    for coin_order in update_coin_order_list:
                        coin_order_model.update_entity(coin_order)

        self.reponse_json_success()


class MachineValueLogHandler(SevenBaseHandler):
    """
    @description: 用户机台配置记录
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):
        act_id = self.get_param("act_id")
        user_open_id = self.get_param("user_open_id")
        machine_info_model = MachineInfoModel()
        machine_value_model = MachineValueModel()
        machine_value_log_model = MachineValueLogModel()

        machine_info_list = machine_info_model.get_list("act_id=%s", params=act_id)
        machine_value_log_list_dict = machine_value_log_model.get_dict_list("act_id=%s and open_id=%s", order_by='create_date desc', params=[act_id, user_open_id])
        machine_value_list = machine_value_model.get_list("act_id=%s and open_id=%s", params=[act_id, user_open_id])

        machine_value_log_groups = []
        for machine_info in machine_info_list:
            machine_value_log_group = {}
            machine_value_log_group["machine_id"] = machine_info.id
            machine_value_log_group["machine_name"] = machine_info.machine_name
            for machine_value in machine_value_list:
                if machine_value.machine_id == machine_info.id:
                    machine_value_log_group["surplus_value"] = machine_value.surplus_value
                    machine_value_log_group["open_value"] = machine_value.open_value
                    continue
            if "surplus_value" not in machine_value_log_group.keys():
                machine_value_log_group["surplus_value"] = 0
            if "open_value" not in machine_value_log_group.keys():
                machine_value_log_group["open_value"] = 0
            machine_value_log_group["machine_value_log_list"] = [i for i in machine_value_log_list_dict if i["machine_id"] == machine_info.id]
            machine_value_log_groups.append(machine_value_log_group)

        self.reponse_json_success(machine_value_log_groups)