# coding:utf-8
# pip3 install requests prettytable docopt colorama

"""12306
Usage:
	格式： <出发站> <到达站> <出发时间>
"""
from prettytable import PrettyTable, ALL
from stations import stations
from docopt import docopt
from colorama import init, Fore, Style
import utils
import requests
import re

"""
获取查询URL
"""
def get_train_url():
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<出发站>'])
    to_station = stations.get(arguments['<到达站>'])
    date = arguments['<出发时间>']
    if from_station is None:
        print('未找到出发站，或出发站无列车信息')
        exit()
    if to_station is None:
        print('未找到到达站，或到达站无列车信息')
        exit()
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station)
    return url

"""
解析数据
"""
def get_train_info(url):
    try:
        r = requests.get(url)
        raw_trains = r.json()['data']['result']
    except:
        # print('数据解析失败，确认信息无误后请重新提交')
        # exit()
        return None

    # print(raw_trains)
    code_dict = utils.list_reverse(stations)
    
    info_list = []
    for raw_train in raw_trains:
        # 循环遍历每辆列车的信息
        data_list = raw_train.split('|')
        # 车次号
        train_no = data_list[3]
        # 出发站
        from_station_code = data_list[6]
        from_station_name = code_dict[from_station_code]
        # 终点站
        to_station_code = data_list[7]
        to_station_name = code_dict[to_station_code]
        # 出发时间
        start_time = data_list[8]
        # 到达时间
        arrive_time = data_list[9]
        # 总耗时
        time_fucked_up = data_list[10]
        # 商务座
        if data_list[32].isdigit() or data_list[32] == '有':
            king_class_seat = Style.BRIGHT + Fore.GREEN +  data_list[32] + Fore.RESET + Style.NORMAL
        else:
            king_class_seat = data_list[32] or Fore.RED +  '--' + Fore.RESET
        # 一等座
        if data_list[31].isdigit() or data_list[31] == '有':
            frist_class_seat = Style.BRIGHT + Fore.GREEN +  data_list[31] + Fore.RESET + Style.NORMAL
        else:
            frist_class_seat = data_list[31] or Fore.RED +  '--' + Fore.RESET
        # 二等座
        if data_list[30].isdigit() or data_list[30] == '有':
            second_class_seat = Style.BRIGHT + Fore.GREEN +  data_list[30] + Fore.RESET + Style.NORMAL
        else:
            second_class_seat = data_list[30] or Fore.RED +  '--' + Fore.RESET
        # 软卧
        if data_list[23].isdigit() or data_list[23] == '有':
            soft_sleep = Style.BRIGHT + Fore.GREEN +  data_list[23] + Fore.RESET + Style.NORMAL
        else:
            soft_sleep = data_list[23] or Fore.RED +  '--' + Fore.RESET
        # 硬卧
        if data_list[28].isdigit() or data_list[28] == '有':
            hard_sleep = Style.BRIGHT + Fore.GREEN +  data_list[28] + Fore.RESET + Style.NORMAL
        else:
            hard_sleep = data_list[28] or Fore.RED +  '--' + Fore.RESET
        # 硬座
        if data_list[29].isdigit() or data_list[29] == '有':
            hard_seat = Style.BRIGHT + Fore.GREEN +  data_list[29] + Fore.RESET + Style.NORMAL
        else:
            hard_seat = data_list[29] or Fore.RED +  '--' + Fore.RESET
        # 无座
        if data_list[26].isdigit() or data_list[26] == '有':
            no_seat = Style.BRIGHT + Fore.GREEN +  data_list[26] + Fore.RESET + Style.NORMAL
        else:
            no_seat = data_list[26] or Fore.RED +  '--' + Fore.RESET

        # 打印查询结果
        info = ( train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up
            ,king_class_seat, frist_class_seat, second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat )
        info_list.append(info)

    return info_list

"""
输出终端
"""
def print_train_info(infos):
    table = PrettyTable( [ Style.BRIGHT + "ID", "车次", "出发站", "到达站", "出发时间", "到达时间", "历时"
        , "商务座", "一等座", "二等座", "软卧", "硬卧", "硬座", "无座" + Style.NORMAL ] )
    table.align["ID"] = "l"
    table.padding_width = 2
    # 绘制表格横线
    table.hrules = ALL
    num = 0
    for info in infos:
        num = num + 1
        # 高铁上色
        if info[0][0] == 'G':
            color_fore_train_no = Fore.YELLOW
        else:
            color_fore_train_no = Fore.WHITE
        
        table.add_row([ Style.BRIGHT + Fore.GREEN +  str(num) + Fore.RESET + Style.NORMAL
            , Style.BRIGHT + color_fore_train_no + info[0] + Fore.RESET + Style.NORMAL, info[1], info[2]
            , info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10], info[11], info[12] ])
    print("\n", table, "\n")


if __name__ == '__main__':
    url = get_train_url()
    info = get_train_info(url)
    while info == None:
        info = get_train_info(url)
    print_train_info(info)
            
