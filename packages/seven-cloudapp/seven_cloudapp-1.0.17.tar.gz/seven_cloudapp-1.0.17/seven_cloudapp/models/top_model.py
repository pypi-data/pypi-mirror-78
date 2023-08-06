# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-08-06 17:10:27
@LastEditTime: 2020-08-07 16:37:02
@LastEditors: HuangJingCan
@Description: 淘宝top接口相关
"""

from seven_framework.config import *
from seven_top import top

from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.seven_model import InvokeResult
from seven_cloudapp.models.seven_model import InvokeResultData


class TopModel():
    """
    @description: 淘宝top接口相关
    """
    def get_now_datetime(self):
        """
        @description: 获取当前时间加8小时
        @return: str
        @last_editors: HuangJingCan
        """
        return TimeHelper.add_hours_by_format_time(hour=8)

    def get_sku_info(self, num_iids, access_token):
        """
        @description: 获取sku信息
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        invoke_result = InvokeResult()
        invoke_result_data = InvokeResultData()

        resp = self.items_seller_list_get_request(num_iids, access_token)

        if "items_seller_list_get_response" in resp.keys():
            if "items" in resp["items_seller_list_get_response"].keys():
                invoke_result_data.success = True
                invoke_result_data.data = resp["items_seller_list_get_response"]
                invoke_result.data = invoke_result_data.__dict__
            else:
                prize = ActPrizeModel().get_entity("goods_id=%s and sku_detail<>'' and is_sku=1", params=int(num_iids))
                if prize:
                    sku_detail = json.loads(prize.sku_detail.replace('\'', '\"'))
                    invoke_result_data.success = True
                    invoke_result_data.data = sku_detail["items_seller_list_get_response"]
                    invoke_result.data = invoke_result_data.__dict__
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "NoSku"
                    invoke_result_data.error_message = "对不起，找不到该商品的sku"
                    invoke_result.data = invoke_result_data.__dict__
        else:
            invoke_result_data.success = True
            invoke_result_data.data = resp
            invoke_result.data = invoke_result_data.__dict__

        return invoke_result

    def get_sku_name(self, num_iids, sku_id, access_token):
        """
        @description: 获取sku名称
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        resp = self.items_seller_list_get_request(num_iids, access_token)

        if "items_seller_list_get_response" in resp.keys():
            if "items" in resp["items_seller_list_get_response"].keys():
                props_names = resp["items_seller_list_get_response"]["items"]["item"][0]["props_name"].split(';')
                for sku in resp["items_seller_list_get_response"]["items"]["item"][0]["skus"]["sku"]:
                    if sku["sku_id"] == sku_id:
                        props_name = [i for i in props_names if sku["properties"] in i]
                        if len(props_name) > 0:
                            self.logger_info.info(props_name[0][(len(sku["properties"]) + 1):])
                            return props_name[0][(len(sku["properties"]) + 1):]
                        else:
                            self.logger_info.info(sku["properties_name"].split(':')[1])
                            return sku["properties_name"].split(':')[1]
        return ""

    def get_taobao_order(self, open_id, access_token):
        """
        @description: 获取淘宝订单
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        all_order = []
        has_next = True

        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.OpenTradesSoldGetRequest()

        req.fields = "tid,status,payment,price,created,orders,num,pay_time"

        req.type = "fixed"
        req.buyer_open_id = open_id
        req.page_size = 10
        req.page_no = 1
        req.use_has_next = "true"

        start_timestamp = TimeHelper.get_now_timestamp() - 90 * 24 * 60 * 60
        start_created = TimeHelper.timestamp_to_format_time(start_timestamp)
        # start_created = "2020-06-01 00:00:00"

        req.start_created = start_created

        while has_next:
            resp = req.getResponse(access_token)
            if "open_trades_sold_get_response" in resp.keys():
                if "trades" in resp["open_trades_sold_get_response"].keys():
                    all_order = all_order + resp["open_trades_sold_get_response"]["trades"]["trade"]
                req.page_no += 1
                has_next = resp["open_trades_sold_get_response"]["has_next"]

        return all_order

    def instantiate_app(self, user_nick, open_id, description, icon, name, template_id, template_version, isfirst, access_token, name_ending):
        """
        @description: 实例化
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.MiniappTemplateInstantiateRequest()

            req.clients = "taobao,tmall"
            req.description = description
            shop_info = self.get_shop(access_token)

            if isfirst == 1:
                app_name = shop_info["shop_seller_get_response"]["shop"]["title"] + name_ending
            else:
                app_name = name

            req.ext_json = "{ \"name\":\"" + app_name + "\"}"
            req.icon = icon
            req.name = app_name
            req.template_id = template_id
            req.template_version = template_version
            resp = req.getResponse(access_token)

            #录入数据库
            result_app = resp["miniapp_template_instantiate_response"]
            app_info_model = AppInfoModel()
            app_info = AppInfo()
            app_info.clients = req.clients
            app_info.app_desc = result_app["app_description"]
            app_info.app_icon = result_app["app_icon"]
            app_info.app_id = result_app["app_id"]
            app_info.app_name = result_app["app_name"]
            app_info.app_ver = result_app["app_version"]
            app_info.app_key = result_app["appkey"]
            app_info.preview_url = result_app["pre_view_url"]
            app_info.template_id = req.template_id
            app_info.template_ver = req.template_version

            if "shop_seller_get_response" in shop_info.keys():
                app_info.store_name = shop_info["shop_seller_get_response"]["shop"]["title"]
                app_info.store_id = shop_info["shop_seller_get_response"]["shop"]["sid"]

            user_seller = self.get_user_seller(access_token)
            if "user_seller_get_response" in user_seller.keys():
                app_info.seller_id = user_seller["user_seller_get_response"]["user"]["user_id"]

            app_info.is_instance = 1
            app_info.store_user_nick = user_nick.split(':')[0]
            app_info.owner_open_id = open_id
            app_info.instance_date = self.get_now_datetime()
            app_info.modify_date = self.get_now_datetime()
            #上线
            online_app_info = self.online_app(app_info.app_id, req.template_id, req.template_version, app_info.app_ver, access_token)
            if "miniapp_template_onlineapp_response" in online_app_info.keys():
                app_info.app_url = online_app_info["miniapp_template_onlineapp_response"]["app_info"]["online_url"]

            app_info.id = AppInfoModel().add_entity(app_info)
            return app_info
        except Exception as ex:
            self.logger_info.info(str(ex))
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=" in content:
                        if "名称已经存在" in content:
                            if isfirst == 1:
                                return self.instantiate_app(user_nick, open_id, description, icon, name, template_id, template_version, 0, access_token, name_ending)
                            else:
                                return {"error": "CreateError", "message": content[len("submsg="):]}
                        return {"error": "CreateError", "message": content[len("submsg="):]}

    def online_app(self, app_id, template_id, template_version, app_version, access_token):
        """
        @description: app上线
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.MiniappTemplateOnlineappRequest()

        req.clients = "taobao,tmall"
        req.app_id = app_id
        req.template_id = template_id
        req.template_version = template_version
        req.app_version = app_version
        resp = req.getResponse(access_token)
        return resp

    def get_shop(self, access_token):
        """
        @description: 获取店铺信息
        @param {type} 
        @return: 
        @last_editors: HuangJingCan
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.ShopSellerGetRequest()

        req.fields = "sid,title,pic_path"
        resp = req.getResponse(access_token)
        return resp

    def get_user_seller(self, access_token):
        """
        @description: 获取关注店铺用户信息
        @param {type} 
        @return: 
        @last_editors: HuangJingCan
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.UserSellerGetRequest()

        req.fields = "user_id,nick,sex"
        resp = req.getResponse(access_token)
        return resp

    def get_dead_date(self, source_app_id, user_nick, access_token):
        """
        @description: 获取过期时间
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        if source_app_id == "":
            return "expire"

        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.VasSubscribeGetRequest()

        req.article_code = config.get_value("article_code")
        req.nick = user_nick
        resp = req.getResponse(access_token)
        if "article_user_subscribe" not in resp["vas_subscribe_get_response"]["article_user_subscribes"].keys():
            return "expire"
        else:
            return resp["vas_subscribe_get_response"]["article_user_subscribes"]["article_user_subscribe"][0]["deadline"]

    def get_token(self, source_app_id, access_token):
        """
        @description: 获取授权token
        @param {type} 
        @return: 
        @last_editors: CaiYouBin
        """
        if source_app_id == "":
            return ""

        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.ItemsOnsaleGetRequest()

        req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
        req.page_no = 1
        req.page_size = 10

        try:
            resp = req.getResponse(access_token)
            return access_token
        except Exception as ex:
            return ""

    def get_goods_list(self, page_index, page_size, goods_name, order_tag, order_by, access_token):
        """
        @description: 导入商品列表
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        invoke_result = InvokeResult()
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemsOnsaleGetRequest()

            req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
            req.page_no = page_index + 1
            req.page_size = page_size
            if goods_name != "":
                req.q = goods_name
            req.order_by = order_tag + ":" + order_by
            resp = req.getResponse(access_token)
            if resp:
                resp["pageSize"] = page_size
                resp["pageIndex"] = page_index

            invoke_result_data.success = True
            invoke_result_data.data = resp
            invoke_result.data = invoke_result_data.__dict__
            return invoke_result
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "NoPower"
                        invoke_result_data.error_message = content[len("submsg="):]
                        invoke_result.data = invoke_result_data.__dict__
                        return invoke_result
                    if "submsg=" in content:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "Error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        invoke_result.data = invoke_result_data.__dict__
                        return invoke_result

    def get_goods_info(self, num_iid, access_token):
        """
        @description: 导入商品列表
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        invoke_result = InvokeResult()
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemSellerGetRequest()

            req.fields = "num_iid,title,nick,pic_url,price,item_img.url,outer_id,sku,approve_status"
            req.num_iid = num_iid

            resp = req.getResponse(access_token)

            invoke_result_data.success = True
            invoke_result_data.data = resp
            invoke_result.data = invoke_result_data.__dict__
            return invoke_result
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "NoPower"
                        invoke_result_data.error_message = content[len("submsg="):]
                        invoke_result.data = invoke_result_data.__dict__
                        return invoke_result
                    if "submsg=该商品已被删除" in content:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "GoodsDel"
                        invoke_result_data.error_message = content[len("submsg="):]
                        invoke_result.data = invoke_result_data.__dict__
                        return invoke_result
                    if "submsg=" in content:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "Error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        invoke_result.data = invoke_result_data.__dict__
                        return invoke_result

    def app_update(self, app_info, app_id, client_template_id, client_ver, access_token):
        """
        @description: app更新
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        invoke_result = InvokeResult()
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.MiniappTemplateUpdateappRequest()
            req.clients = "taobao,tmall"
            req.app_id = app_id
            req.template_id = client_template_id
            req.template_version = client_ver
            resp = req.getResponse(access_token)
            if resp and ("miniapp_template_updateapp_response" in resp.keys()):
                app_version = resp["miniapp_template_updateapp_response"]["app_version"]
                online_app_info = self.online_app(app_id, client_template_id, client_ver, app_version, access_token)
                if "miniapp_template_onlineapp_response" in online_app_info.keys():
                    app_info.app_ver = resp["miniapp_template_updateapp_response"]["app_version"]
                    app_info.template_ver = client_ver
                    app_info.modify_date = self.get_now_datetime()
                    AppInfoModel().update_entity(app_info)

            invoke_result_data.success = True
            invoke_result.data = invoke_result_data.__dict__
            return invoke_result, app_info
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "NoPower"
                        invoke_result_data.error_message = content[len("submsg="):]
                        invoke_result.data = invoke_result_data.__dict__
                        return invoke_result, None
                    if "submsg=" in content:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "Error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        invoke_result.data = invoke_result_data.__dict__
                        return invoke_result, None

    def items_seller_list_get_request(self, num_iids, access_token):
        """
        @description: 
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.ItemsSellerListGetRequest()
        req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
        req.num_iids = num_iids
        resp = req.getResponse(access_token)
        return resp