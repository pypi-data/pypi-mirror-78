# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-05 17:10:27
@LastEditTime: 2020-06-28 17:16:26
@LastEditors: CaiYouBin
@Description: 统计相关
"""

from seven_cloudapp.models.db_models.behavior.behavior_log_model import *
from seven_cloudapp.models.db_models.behavior.behavior_orm_model import *
from seven_cloudapp.models.db_models.behavior.behavior_report_model import *
import decimal


class BehaviorModel():
    """
    @description: 统计相关
    """
    def report_behavior(self, app_id, act_id, open_id, owner_open_id, behavior_key, behavior_value):
        """
        @description: 上报行为记录
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        behavior_orm_model = BehaviorOrmModel()
        behavior_log_model = BehaviorLogModel()
        behavior_report_model = BehaviorReportModel()
        orm = behavior_orm_model.get_entity("((act_id=%s and is_common=0) or is_common=1) and key_name=%s", params=[act_id, behavior_key])
        if not orm:

            return "NotOrm"
        if orm.is_repeat == 1:
            behavior_log = behavior_log_model.get_entity("orm_id=%s and act_id=%s and open_id=%s and to_days(create_date) = to_days(now())", params=[orm.id, act_id, open_id])
            if not behavior_log:

                behavior_report = behavior_report_model.get_entity("act_id=%s and app_id=%s and key_name=%s and to_days(create_date) = to_days(now())", params=[act_id, app_id, behavior_key])
                if not behavior_report:
                    behavior_report = BehaviorReport()
                    behavior_report.app_id = app_id
                    behavior_report.act_id = act_id
                    # behavior_report.owner_open_id
                    behavior_report.key_name = behavior_key
                    behavior_report.key_value = behavior_value
                    behavior_report.create_year = (datetime.datetime.now() + datetime.timedelta(hours=8)).year
                    behavior_report.create_month = (datetime.datetime.now() + datetime.timedelta(hours=8)).month
                    behavior_report.create_day = (datetime.datetime.now() + datetime.timedelta(hours=8)).day
                    behavior_report.create_date = TimeHelper.add_hours_by_format_time(hour=8)
                    behavior_report_model.add_entity(behavior_report)
                else:
                    behavior_report.key_value = decimal.Decimal(behavior_report.key_value) + behavior_value
                    behavior_report_model.update_entity(behavior_report)
        else:
            behavior_report = behavior_report_model.get_entity("act_id=%s and app_id=%s and key_name=%s and to_days(create_date) = to_days(now())", params=[act_id, app_id, behavior_key])
            if not behavior_report:
                behavior_report = BehaviorReport()
                behavior_report.app_id = app_id
                behavior_report.act_id = act_id
                # behavior_report.owner_open_id
                behavior_report.key_name = behavior_key
                behavior_report.key_value = behavior_value
                behavior_report.create_year = (datetime.datetime.now() + datetime.timedelta(hours=8)).year
                behavior_report.create_month = (datetime.datetime.now() + datetime.timedelta(hours=8)).month
                behavior_report.create_day = (datetime.datetime.now() + datetime.timedelta(hours=8)).day
                behavior_report.create_date = TimeHelper.add_hours_by_format_time(hour=8)
                behavior_report_model.add_entity(behavior_report)
            else:
                behavior_report.key_value = decimal.Decimal(behavior_report.key_value) + behavior_value
                behavior_report_model.update_entity(behavior_report)

        new_behavior_log = BehaviorLog()
        new_behavior_log.app_id = app_id
        new_behavior_log.act_id = act_id
        new_behavior_log.open_id = open_id
        new_behavior_log.orm_id = orm.id
        new_behavior_log.inc_value = behavior_value
        new_behavior_log.create_date = TimeHelper.add_hours_by_format_time(hour=8)

        behavior_log_model.add_entity(new_behavior_log)