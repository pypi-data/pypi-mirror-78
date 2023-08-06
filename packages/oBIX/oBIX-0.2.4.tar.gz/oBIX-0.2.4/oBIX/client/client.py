import sys
import logging
import requests
import xml.etree.ElementTree as xmlElement
import urllib3
import xmltodict
from oBIX.common.DataType import DataType
from datetime import datetime


class Client:
    __host = ""
    __user_name = ""
    __password = ""
    __enable_proxy = False
    __proxy_dict = None

    __logger = None

    def __init__(self, host, user_name, password, enable_proxy=False, proxy_dict=None):
        self.__host = host
        self.__user_name = user_name
        self.__password = password
        self.__enable_proxy = enable_proxy
        self.__proxy_dict = proxy_dict
        self.__init_log()

    def __init_log(self, log_level=logging.DEBUG, enable_console=True, enable_file=True, file_name="oBIX.log"):
        log_instance = logging.getLogger("log")
        log_instance.setLevel(log_level)
        log_format = "[%(levelname)-8s] %(asctime)s >> %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(log_format, date_format)
        if enable_file:
            file_handler = logging.FileHandler(file_name, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            log_instance.addHandler(file_handler)

        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            log_instance.addHandler(console_handler)
        self.__logger = log_instance

    def __serialize_one_data(self, value, data_type: DataType, parameter=None):
        try:
            result = ""
            if data_type == DataType.bool:
                result = '<bool val="{0}"/>'.format(str(bool(value)).lower())
            elif data_type == DataType.int:
                result = '<int val="{0}"/>'.format(int(value))
            elif data_type == DataType.real:
                result = '<real val="{0}"/>'.format(float(value))
            elif data_type == DataType.str:
                result = '<str val="{0}"/>'.format(str(value))
            elif data_type == DataType.enum:
                result = '<enum range="{0}" val="{1}"/>'.format(parameter, str(value))
            elif data_type == DataType.abs_time:
                # 2005-03-09T13:30:00Z
                result = '<abstime val="{0}"/>'.format(value.strftime('%Y-%m-%dT%H:%M:%S%Z'))
            elif data_type == DataType.rel_time:
                result = '<reltime val="{0}"/>'.format(str(value))
            elif data_type == DataType.href:
                result = '<obj href="{0}">'.format(str(parameter))
                if isinstance(value, int):
                    result = result + '<int  val="{0}"/>'.format(int(value))
                elif isinstance(value, float):
                    result = result + '<real val="{0}"/>'.format(float(value))
                elif isinstance(value, bool):
                    result = result + '<bool val="{0}"/>'.format(bool(value))
                else:
                    result = result + '<obj val="{0}"/>'.format(str(value))
                result = result + "</obj>"
            else:
                result = ""
            return result
        except Exception as e:
            self.__logger.error(e)
            return ""

    def __serialize_data(self, value, data_type: DataType, parameter=None):
        try:
            result = ""
            if data_type == DataType.list:
                if not isinstance(parameter, DataType):
                    self.__logger.error("The type of the current <value> is an [DataType.list]."
                                        " Please use the <parameter> to specify the data type of the list element.")
                    return ""
                type_str = ""
                if data_type == DataType.bool:
                    type_str = "bool"
                elif data_type == DataType.int:
                    type_str = "int"
                elif data_type == DataType.real:
                    type_str = "real"
                elif data_type == DataType.str:
                    type_str = "str"
                elif data_type == DataType.enum:
                    type_str = "enum"
                elif data_type == DataType.abs_time:
                    type_str = "abstime"
                elif data_type == DataType.rel_time:
                    type_str = "reltime"
                result = '<list of="obix:{0}">\n'.format(type_str)
                for one in value:
                    element = self.__serialize_one_data(one, parameter)
                    result = result + "  " + element + "\n"
                result = result + "</list>"
                return result
            else:
                result = self.__serialize_one_data(value, data_type, parameter)
            return result
        except Exception as e:
            self.__logger.error(e)
            return ""

    def __convert_to_type(self, str_value: str, data_type: DataType):
        if data_type == DataType.real:
            return float(str_value)
        elif data_type == DataType.bool:
            return bool(str_value)
        elif data_type == DataType.int:
            return int(str_value)
        else:
            return str_value

    def __get_url(self, url_path: str, operation=""):
        if url_path[0] != "/":
            url_path = "/" + url_path
        if url_path[-1:] != "/":  # 最后一个字符是否是 /
            url_path = url_path + "/"
        if operation == "":
            url = "https://{0}/obix{1}".format(self.__host, url_path)
        else:
            url = "https://{0}/obix{1}{2}".format(self.__host, url_path, operation)
        return url

    def read_point(self, point_path: str):
        try:
            url = self.__get_url(point_path)
            urllib3.disable_warnings()
            if self.__enable_proxy:
                response = requests.get(url, auth=(self.__user_name, self.__password), proxies=self.__proxy_dict,
                                        verify=False)
            else:
                response = requests.get(url, auth=(self.__user_name, self.__password), verify=False)
            if response.status_code == 200:
                xml_root = xmlElement.fromstring(response.text)
                xml_root_str = xmlElement.tostring(xml_root, encoding="utf-8")
                return xmltodict.parse(xml_root_str)
            else:
                return None
        except Exception as e:
            self.__logger.error(e)
            return None

    def read_point_value(self, point_path: str):
        try:
            point_dict = self.read_point(point_path)
            if point_dict:
                first_key = list(point_dict.keys())[0]
                first_key_value_str = point_dict[first_key]["@val"]
                if "real" in first_key:
                    return float(first_key_value_str)
                elif "bool" in first_key:
                    return bool(first_key_value_str)
                elif "int" in first_key:
                    return int(first_key_value_str)
                else:
                    return first_key_value_str
            else:
                return None
        except Exception as e:
            self.__logger.error(e)
            return None

    def set_point_value(self, point_path: str, value, data_type: DataType, parameter=None):
        return self.__operate_point(point_path, "set", value, data_type, parameter)

    def set_point_auto(self, point_path: str, data_type: DataType, parameter=None):
        return self.__operate_point(point_path, "auto", "0", data_type, parameter)

    # not work
    def override_point(self, point_path: str, value):
        self.__operate_point(point_path, "override", value, DataType.href, "/obix/def/control:NumericOverride /obix/def/control:Override")

    def __operate_point(self, url_path: str, operation: str, value, data_type: DataType, parameter=None):
        try:
            url = self.__get_url(url_path, operation)
            urllib3.disable_warnings()
            post_data = self.__serialize_data(value, data_type, parameter)
            if not post_data:
                self.__logger.error("Operate Point Failed: POST Data serialization failed!")
                return False
            if self.__enable_proxy:
                response = requests.post(url, auth=(self.__user_name, self.__password), data=post_data,
                                         proxies=self.__proxy_dict, verify=False)
            else:
                response = requests.post(url, auth=(self.__user_name, self.__password), data=post_data, verify=False)
            if response.status_code == 200:
                xml_root = xmlElement.fromstring(response.text)
                xml_root_str = xmlElement.tostring(xml_root, encoding="utf-8")
                root = xmltodict.parse(xml_root_str)
                first_key = list(root.keys())[0]
                if "err" in first_key:
                    error_msg = root[first_key]["@display"]
                    self.__logger.error("Operate Point Failed: {0}".format(error_msg))
                    return error_msg
                else:
                    return "OK"
            else:
                self.__logger.error("Operate Point Failed: Response StatusCode is {0}".format(response.status_code))
                return False
        except Exception as e:
            self.__logger.error("Operate Point Failed: Trigger exception！")
            self.__logger.error(e)
            return False

    def write_point(self, url: str, value, data_type: DataType, parameter=None):
        self.set_point_value(url, value, data_type, parameter)

    def read_history(self, station, point, start_time: datetime, end_time: datetime = None, limit=None):
        try:
            urllib3.disable_warnings()
            start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.000%Z").replace("UTC", "")
            if end_time is None:
                end_time_str = ""
            else:
                end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.000%Z").replace("UTC", "")
            if isinstance(limit, int) and limit > 0:
                url = "https://{0}/obix/histories/{1}/{2}/~historyQuery?start={3}&limit={4}"\
                    .format(self.__host, station, point, start_time_str, limit)
            else:
                url = "https://{0}/obix/histories/{1}/{2}/~historyQuery?start={3}&end={4}" \
                    .format(self.__host, station, point, start_time_str, end_time_str)
            if self.__enable_proxy:
                response = requests.get(url, auth=(self.__user_name, self.__password), proxies=self.__proxy_dict,
                                        verify=False)
            else:
                response = requests.get(url, auth=(self.__user_name, self.__password), verify=False)
            if response.status_code == 200:
                root = xmltodict.parse(response.text)
                temp_list = root["obj"]["list"]
                if "obj" not in temp_list:
                    return []
                data_list = root["obj"]["list"]["obj"]
                result = []
                for data in data_list:
                    one = dict()
                    for key in list(data.keys()):
                        if key == "abstime":
                            one["timeStamp"] = datetime.strptime(str(data[key]["@val"]), "%Y-%m-%dT%H:%M:%S.%f%z")
                        elif key == "real":
                            one["value"] = float(data[key]["@val"])
                        elif key == "bool":
                            one["value"] = bool(data[key]["@val"])
                        elif key == "int":
                            one["value"] = int(data[key]["@val"])
                        else:
                            one["value"] = data[key]["@val"]
                    result.append(one)
                return result
            else:
                return None
        except Exception as e:
            self.__logger.error(e)
            return None

    def __filter_property(self, src: dict, property_name:str):
        for key in src.keys():
            if "@name" in src[key]:
                if src[key]["@name"] == property_name:
                    return src[key]
        return None

    def read_alarms(self, start_time: datetime, end_time: datetime = None, limit=None):
        try:
            urllib3.disable_warnings()
            url = "https://{0}/obix/config/Services/AlarmService/~alarmQuery/".format(self.__host)
            post_data = '<obj is="obix:AlarmFilter"> '

            start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.000%Z").replace("UTC", "")
            post_data = post_data + ' <abstime name="start" val="{0}"/> '.format(start_time_str)
            if end_time is None:
                end_time_str = ""
            else:
                end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.000%Z").replace("UTC", "")
                post_data = post_data + ' <abstime name="end" val="{0}"/> '.format(end_time_str)
            if isinstance(limit, int) and limit > 0:
                post_data = post_data + '  <int name="limit" val="{0}"/>'.format(limit)

            post_data = post_data + " </obj>"
            if self.__enable_proxy:
                response = requests.post(url, auth=(self.__user_name, self.__password), data=post_data,
                                         proxies=self.__proxy_dict, verify=False)
            else:
                response = requests.post(url, auth=(self.__user_name, self.__password), data=post_data, verify=False)
            if response.status_code == 200:
                root = xmltodict.parse(response.text)
                temp_list = root["obj"]["list"]
                if "obj" not in temp_list:
                    return []
                data_list = root["obj"]["list"]["obj"]
                # if isinstance(data_list, []):
                #
                result = []
                for data in data_list:
                    one = dict()
                    value_dict = self.__filter_property(data, "alarmValue")
                    if value_dict is not None:
                        key = value_dict["@val"]
                        if key == "real":
                            one["value"] = float(data[key]["@val"])
                        elif key == "bool":
                            one["value"] = bool(data[key]["@val"])
                        elif key == "int":
                            one["value"] = int(data[key]["@val"])
                    if "abstime" in data:
                        one["timeStamp"] = datetime.strptime(str(data["abstime"]["@val"]), "%Y-%m-%dT%H:%M:%S.%f%z")
                    if "str" in data:
                        one["str"] = data["str"]
                    result.append(one)
                return result
            else:
                return None
        except Exception as e:
            self.__logger.error(e)
            return None
