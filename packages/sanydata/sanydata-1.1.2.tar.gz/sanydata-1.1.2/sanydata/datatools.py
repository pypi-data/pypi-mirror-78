#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Team : SANY Heavy Energy DataTeam
# @Time    : 2020/8/05 17:37 下午
# @Author  : THao

import time
import json
import sqlite3

import pandas as pd
import data_message_pb2


class DataTools(object):
    # This programme is to get data.
    PROGRAMME = 'DataTools'
    VERSION = '1.0.2'

    def get_files_list(self, stub, regex='@@TYSFCB/@@202007@@fault@@.csv'):
        """
        regex：所要查询数据的‘正则’表达式，其中@@符号为通配符
        return：匹配到的所有文件列表
        """

        dainput = data_message_pb2.GetFileListInput(regex=regex)
        res = stub.GetFileList(dainput, timeout=20000)
        res = json.loads(res.output)
        return res

    def get_data(self, stub, file_list, columns=None):
        """
        file_list：所要获取文件列表
        columns：需要的字段，默认加载所有字段
        return：所查询数据合并成的pandas.DataFrmae，在原有的列上增加turbine_num列，用来标识机组号，例：001
        """
        if len(file_list) > 0 and isinstance(file_list, list):
            df_all = list()
            import os
            import zipfile
            import io
            from io import StringIO
            dainput = data_message_pb2.GetTargetFileInput(filelist=json.dumps(file_list))
            if file_list[0].split('.')[-1] == 'parquet':
                for i in stub.GetTargetFile(dainput, timeout=20000):
                    try:
                        f = zipfile.ZipFile(file=io.BytesIO(i.output))
                        file_name = f.namelist()[0]
                        turbine_num = file_name.split('#')[0]
                        pure_data = f.read(file_name)
                        fio = io.BytesIO(pure_data)
                        with open('./parquet_file_grpc_temp.parquet', "wb") as outfile:
                            outfile.write(fio.getbuffer())
                        df = pd.read_parquet('./parquet_file_grpc_temp.parquet', columns=columns)
                        df['turbine_num'] = turbine_num
                        os.remove('./parquet_file_grpc_temp.parquet')
                        df_all.append(df)
                    except Exception as e:
                        print(e)
            else:
                for i in stub.GetTargetFile(dainput, timeout=20000):
                    try:
                        f = zipfile.ZipFile(file=io.BytesIO(i.output))
                        file_name = f.namelist()[0]
                        turbine_num = file_name.split('_')[1]
                        pure_data = f.read(file_name)
                        try:
                            df = pd.read_csv(StringIO(pure_data.decode('gbk')))
                        except:
                            df = pd.read_csv(StringIO(pure_data.decode('utf-8')))
                        df['turbine_num'] = turbine_num
                        if columns:
                            df_all.append(df[columns + ['turbine_num']])
                        else:
                            df_all.append(df)
                    except Exception as e:
                        print(e)
            if len(df_all) > 0:
                df_all = pd.concat(df_all)
                df_all = df_all.reset_index(drop=True)
        else:
            df_all = '将检查传入的文件列表'
        return df_all

    def return_result(self, stub, project_name, wind_farm, data_start_time, data_end_time,
                      turbine_type=None, turbine_num=None, status=None, result=None,
                      result_json=None, upload_fig_path=None, upload_log_path=None,
                      upload_file_path=None, local_fig_path=None, local_log_path=None,
                      local_file_path=None, model_version=None, project_id=None):

        """
        project_name：模型英文名，不可省略
        wind_farm：风场拼音缩写，不可省略
        data_start_time：模型中使用的数据开始时间，不可省略（方便后续排查问题查询，格式统一为‘%Y-%m-%d %H:%M:%S’）
        data_end_time：模型中使用的数据结束时间，不可省略（格式统一为‘%Y-%m-%d %H:%M:%S’）
        turbine_type：机组型号（字符串，例如：‘14125’），可省略
        turbine_num：机组号（字符串，例如：01,02），可省略
        status：判断状态，共分为三种：正常、告警、故障（目的是前端显示颜色，分别为无色、黄色、红色）
        result：模型判断结果（例如：0.8、90，不可判断等），可省略
        result_json：模型产生的其他信息，json格式，可省略（主要留作后续给前段产生动态图的json数据）
        upload_fig_path：模型产生图片云端保存位置，可省略
        upload_log_path：模型产生日志云端保存位置，可省略
        upload_file_path：模型其他文件云端保存位置，可省略
        local_fig_path：模型产生的图片本地保存位置，可省略
        local_log_path：模型产生的日志本地保存位置，可省略
        local_file_path：模型产生的其他文件本地保存位置，可省略
        model_version：模型版本号（例如：1.0.0），可省略，(不建议省略)
        project_id：模型id号（例如：10001），可省略(目前可省略，后续统一之后再设置)
        return：返回为int数字，如果成果，则返回0，如果失败，则返回1
        注意：
        1）模型执行过程将产生的图片、日志、其他文件等暂保存为本地位置，最终通过调用接口，传入相关参数后，接口会自动将本地文件传入云端，并删除本地文件
        2）模型上传文件统一格式为：fig、log、file/{模型名字，project_name}/{wind_farm,风场名}/**.png、**.log、**.csv、其他；（**代表最终文件命名，命名时应尽可能说明机组号、模型所使用数据时间等信息，可以对模型每次执行结果进行区分）
        3）模型本地保存统一格式为：/tmp/sanydata_frpc_**.png、sanydata_frpc_**.log、sanydata_frpc_**.csv、其他（上述中**代表最终文件命名，命名时应尽可能避免多文件保存到本地时进行覆盖，建议采用当前时间）

        """
        import datetime
        import os
        model_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model_start_time = os.getenv('ModelStartTime')
        task_id = int(os.getenv('TaskId'))
        if not model_version:
            model_version = os.getenv('ProjectVersion')

        fig_fio = None
        log_fio = None
        file_fio = None
        # 本地图片处理
        if local_fig_path:
            with open(local_fig_path, 'rb') as f:
                fig_fio = f.read()
            os.remove(local_fig_path)
        # 本地日志处理
        if local_log_path:
            with open(local_log_path, 'rb') as f:
                log_fio = f.read()
            os.remove(local_log_path)
        # 本地其他文件处理
        if local_file_path:
            with open(local_file_path, 'rb') as f:
                file_fio = f.read()
            os.remove(local_file_path)

        data_input = data_message_pb2.ReturnResultInput(projectname=project_name,
                                                        windfarm=wind_farm, turbinetype=turbine_type, turbine=turbine_num,
                                                        DataStartTime=data_start_time, DataEndTime=data_end_time,
                                                        ModeStartTime=model_start_time, ModeEndTime=model_end_time,
                                                        projectid=project_id, projectversion=model_version, task_id=task_id,
                                                        result=result, resultjson=result_json, status=status,
                                                        uploadfigpath=upload_fig_path, uploadlogpath=upload_log_path,
                                                        uploadfilepath=upload_file_path,
                                                        fig=fig_fio, log=log_fio, file=file_fio)
        res = stub.ReturnResult(data_input, timeout=20000)
        return json.loads(res.code)


class WindFarmInf(object):
    # This programme is to get wind farm information.
    PROGRAMME = 'WindFarmInf'
    VERSION = '1.0.0'

    def __init__(self, sql_file='/tmp/1597716056484sqlite.sqlite'):
        self.sql_file = sql_file
        self.conn = sqlite3.connect(self.sql_file)
        self.df_wind_farm_turbine = pd.read_sql('select * from wind_farm_turbine', con=self.conn)
        self.df_turbine_type_powercurve = pd.read_sql('select * from turbine_type_powercurve', con=self.conn)
        self.conn.close()

    def get_rated_power_by_turbine(self, farm, turbine_num):
        """
        farm：需要查询的风场，例：'TYSFCA'
        turbine_num：需要查询的机组号，例：'001'
        return：所查询机组的额定功率，例：2500
        """

        df_turbine = self.df_wind_farm_turbine.query('pinyin_code == @farm & inner_turbine_name == @turbine_num')
        if len(df_turbine) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine_num)
        else:
            result = df_turbine['rated_power'].unique().tolist()[0]
            if str(result) not in ['nan', 'None']:
                result = float(result)
            else:
                result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine_num)

        return result

    def get_power_curve_by_turbine(self, farm, turbine_num):
        """
        farm：需要查询的风场，例：'TYSFCA'
        turbine_num：需要查询的机组号，例：'001'
        return：所查询机组的理论功率曲线,返回pandas.DataFrame,columns=['Wind', 'Power']
        """

        df_turbine = self.df_wind_farm_turbine.query('pinyin_code == @farm & inner_turbine_name == @turbine_num')
        if len(df_turbine) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine_num)
        else:
            turbine_id = df_turbine['turbine_id'].values[0]
            farm_id = df_turbine['farm_id'].values[0]
            df_power_curve = self.df_turbine_type_powercurve.query('farm_id == @farm_id & turbine_id == @turbine_id')
            if len(df_power_curve) == 0:
                result = '数据库表turbine_type_powercurve中缺少 {}_{} 机组相关id信息'.format(farm, turbine_num)
            else:
                power_curve = df_power_curve['power_curve'].unique().tolist()[0]
                if power_curve:
                    result = dict()
                    wind = list(json.loads(power_curve).keys())
                    wind = [float(x) for x in wind]
                    wind.sort()
                    power = list(json.loads(power_curve).values())
                    power = [float(x) for x in power]
                    power.sort()
                    result['Wind'] = wind
                    result['Power'] = power
                    result = pd.DataFrame(result)
                else:
                    result = '数据库表turbine_type_powercurve中缺少 {}_{} 机组理论功率曲线信息'.format(farm, turbine_num)

        return result

    def get_types_by_farm(self, farm):
        """
        farm：需要查询的风场，例：'TYSFCA'
        return：所查询风场的机型list
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            farm_id = df_farm['farm_id'].unique().tolist()[0]
            df_turbin_types = self.df_turbine_type_powercurve.query('farm_id == @farm_id')
            if len(df_turbin_types) == 0:
                result = '数据库表turbine_type_powercurve中缺少 {} 风场相关id信息'.format(farm)
            else:
                result = df_turbin_types['type_name'].unique().tolist()
                if str(result) in ['nan', 'None']:
                    result = '数据库表turbine_type_powercurve中缺少 {} 风场相关id信息'.format(farm)

        return result

    def get_turbines_by_farm(self, farm):
        """
        farm：需要查询的风场，例：'TYSFCA'
        return：所查询风场下所有风机号list
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            result = df_farm['inner_turbine_name'].unique().tolist()
            if str(result) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
            else:
                result.sort()

        return result

    def get_turbines_by_type(self, farm, type_name):
        """
        farm：需要查询的风场，例：'TYSFCA'
        type_name：需要查询的机组号，例：'SE8715'
        return：所查询风场与机型下所有风机号list
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            farm_id = df_farm['farm_id'].unique().tolist()[0]
            df_turbin_type = self.df_turbine_type_powercurve.query('farm_id == @farm_id & type_name == @type_name')
            if len(df_turbin_type) == 0:
                result = '数据库表turbine_type_powercurve中缺少 {} 风场相关信息'.format(farm)
            else:
                turbines = df_turbin_type['turbine_id'].unique().tolist()
                result = df_farm.query('turbine_id in @turbines')['inner_turbine_name'].unique().tolist()
                if str(result) in ['nan', 'None']:
                    result = '数据库表turbine_type_powercurve中缺少 {} 风场相关信息'.format(farm)
                else:
                    result.sort()

        return result

    def get_power_curve_by_type(self, farm, type_name):
        """
        farm：需要查询的风场，例：'TYSFCA'
        tb_type：需要查询的机组型号，例：'SE8715'
        return：所查询机型的理论功率曲线,返回pandas.DataFrame,columns=['Wind', 'Power']
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 型号机组信息'.format(farm, type_name)
        else:
            farm_id = df_farm['farm_id'].values[0]
            df_power_curve = self.df_turbine_type_powercurve.query('farm_id == @farm_id & type_name == @type_name')
            if len(df_power_curve) > 0:
                power_curve = df_power_curve['power_curve'].unique().tolist()[0]
                if power_curve:
                    result = dict()
                    wind = list(json.loads(power_curve).keys())
                    wind = [float(x) for x in wind]
                    wind.sort()
                    power = list(json.loads(power_curve).values())
                    power = [float(x) for x in power]
                    power.sort()
                    result['Wind'] = wind
                    result['Power'] = power
                    result = pd.DataFrame(result)
                else:
                    result = '数据库表turbine_type_powercurve中缺少 {}_{} 型号机组理论功率曲线信息'.format(farm, type_name)
            else:
                result = '数据库表turbine_type_powercurve中缺少 {}_{} 型号机组相关信息'.format(farm, type_name)

        return result

    def get_chinese_name_by_farm(self, farm):
        """
        farm：需要查询的风场，例：'TYSFCA'
        return：所查询风场的中文名，如果数据库中不存在中文名，则返回字符串'None'
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            result = str(df_farm['farm_name'].unique()[0])
            if str(result) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)

        return result

    def get_py_code_by_farm(self, chinese_name):
        """
        chinese_name：需要查询的风场的中文名，例：'太阳山二期'
        return：所查询风场的拼音缩写，如果数据库中不存在拼音缩写，则返回字符串'None'
        """

        df_farm = self.df_wind_farm_turbine.query('farm_name == @chinese_name')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(chinese_name)
        else:
            result = str(df_farm['pinyin_code'].unique()[0])
            if str(result) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(chinese_name)

        return result

