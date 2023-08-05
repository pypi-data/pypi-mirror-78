# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-12 20:04:54
@LastEditTime: 2020-08-20 17:48:53
@LastEditors: HuangJingCan
@Description: 用户相关
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.db_models.login.login_log_model import *
from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.seven_model import *

from seven_cloudapp.libs.customize.seven import *


class LoginHandler(SevenBaseHandler):
    """
    @description: 登录处理
    """
    @filter_check_params("open_id")
    def get_async(self):
        """
        @description: 登录日志入库
        @param open_id：用户唯一标识
        @param user_nick：用户昵称
        @return: 
        @last_editors: HuangJingCan
        """
        # 用户唯一标识
        open_id = self.get_param("open_id")
        # 用户昵称
        user_nick = self.get_param("user_nick", "")
        # 小程序id
        source_app_id = self.get_param("source_app_id")

        request_params = str(self.request_params)

        if user_nick == "":
            return self.reponse_json_success()

        login_log_model = LoginLogModel()
        login_log = login_log_model.get_entity("open_id=%s", params=open_id)

        is_add = False
        if not login_log:
            is_add = True
            login_log = LoginLog()

        login_log.open_id = open_id
        login_log.user_nick = user_nick
        if user_nick.__contains__(":"):
            login_log.store_user_nick = user_nick.split(":")[0]
            login_log.is_master = 0
        else:
            login_log.store_user_nick = user_nick
            login_log.is_master = 1
        login_log.request_params = request_params
        login_log.modify_date = self.get_now_datetime()

        if is_add:
            login_log.create_date = login_log.modify_date
            login_log.id = login_log_model.add_entity(login_log)
        else:
            login_log_model.update_entity(login_log)

        self.reponse_json_success()


class UserStatusHandler(SevenBaseHandler):
    """
    @description: 更新用户状态
    """
    @filter_check_params("userid,user_state")
    def get_async(self):
        """
        @description: 更新用户状态
        @param userid：用户id
        @param user_state：用户状态
        @return: 
        @last_editors: HuangJingCan
        """
        user_id = int(self.get_param("userid"))
        user_state = int(self.get_param("user_state"))
        modify_date = self.get_now_datetime()
        relieve_date = self.get_now_datetime()

        UserInfoModel().update_table("user_state=%s,modify_date=%s,relieve_date=%s", "id=%s", [user_state, modify_date, relieve_date, user_id])

        self.reponse_json_success()


class UserListHandler(SevenBaseHandler):
    """
    @description: 用户列表
    @param {type} 
    @return: 
    @last_editors: HuangJingCan
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取用户列表
        @param user_id：用户id
        @return: 
        @last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", "0"))
        page_size = int(self.get_param("page_size", "10"))
        user_nick = self.get_param("nick_name")
        act_id = int(self.get_param("act_id", "0"))
        condition = "act_id=%s"
        params = [act_id]
        if user_nick:
            user_nick = f"%{user_nick}%"
            condition += " AND user_nick LIKE %s"
            params.append(user_nick)

        page_list, total = UserInfoModel().get_dict_page_list("id,act_id,open_id,user_nick,pay_price,user_state", page_index, page_size, condition, order_by="id desc", params=params)

        if page_list:
            where = SevenHelper.get_condition_by_id_list("open_id", [i["open_id"] for i in page_list])
            dict_machine_value_list = MachineValueModel().get_dict_list(f"act_id={act_id} AND {where}", "open_id", field="open_id,sum(open_value) as open_value,sum(surplus_value) as surplus_value")
            for i in range(0, len(dict_machine_value_list)):
                dict_machine_value_list[i]["open_value"] = int(dict_machine_value_list[i]["open_value"])
                dict_machine_value_list[i]["surplus_value"] = int(dict_machine_value_list[i]["surplus_value"])
            new_dict_list = SevenHelper.merge_dict_list(page_list, "open_id", dict_machine_value_list, "open_id", "open_value,surplus_value")
            page_info = PageInfo(page_index, page_size, total, new_dict_list)

            self.reponse_json_success(page_info)
        else:
            self.reponse_json_success()