from datetime import datetime

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from monitor.collect.collector import Asm
from monitor.utils.config import CONFIG
from monitor.utils.log import log_init
from monitor.utils.exception import AsmError

LOG = log_init(__name__)

codes = CONFIG.codes_config
sites = CONFIG.sites_config
countryCode = CONFIG.country_code_config
cityCode = CONFIG.city_code_config


def set_column(worksheet, columns):
    for column in columns:
        worksheet.set_column(column[0], column[1], column[2])


def write_cell(worksheet, cells):
    for cell in cells:
        worksheet.write_string(cell[0], cell[1], cell[2], cell[3])


def merge_cell(worksheet, cells):
    for cell in cells:
        worksheet.merge_range(cell[0], cell[1], cell[2], cell[3], cell[4],
                              cell[5])


def write_number(worksheet, cells):
    for cell in cells:
        worksheet.write_number(cell[0], cell[1], cell[2], cell[3])


def title_style(cell, color, positions):
    cell.set_bg_color(color)
    cell.set_font_name("宋体")
    cell.set_font_size(12)
    cell.set_bold()
    cell.set_bottom(1)
    cell.set_top(1)
    cell.set_left(1)
    cell.set_right(1)
    for position in positions:
        cell.set_align(position)


def set_font(cell, size, name, border):
    cell.set_font_size(size)
    cell.set_font_name(name)
    cell.set_border(border)


def create_extra_table(workbook, title_style, col_title_style):
    dates = datetime.today().strftime("%Y-%m-%d")
    worksheet = workbook.add_worksheet("手工监测数据")
    worksheet.merge_range(1, 1, 1, 6, "网站访问-手工监测数据统计", title_style)
    worksheet.set_row(1, 54)
    columns = [(1, 1, 12), (2, 2, 17), (3, 3, 29), (4, 4, 13), (5, 5, 18),
               (6, 6, 18)]
    set_column(worksheet, columns)
    cells = [(3, 1, "监测时间", col_title_style), (3, 2, "监测站点", col_title_style),
             (3, 3, "站点网址", col_title_style), (3, 4, "监测工具", col_title_style),
             (3, 5, "首页相应时间(s)", col_title_style),
             (3, 6, "网址是否可访问", col_title_style)]
    write_cell(worksheet, cells)

    mergeraw = workbook.add_format({"border": 1})
    mergeraw.set_align("center")
    mergeraw.set_align("vcenter")
    mergeraw.set_font_size(12)
    mergeraw.set_font_name("宋体")

    sitestyle = workbook.add_format(
        {"valign": "vcenter", "border": 1, "font_size": 12})
    commonstyle = workbook.add_format({"font_size": 12, "border": 1})

    cells = [
        (4, 1, 19, 1, "%s" % dates, mergeraw),
        (4, 2, 7, 2, "PlatON(京东)", mergeraw),
        (8, 2, 11, 2, "PlatON(东南亚)", mergeraw),
        (12, 2, 15, 2, "ONT本体(东南亚)", mergeraw),
        (16, 2, 19, 2, "Ethereum(以太坊)", mergeraw),
        (4, 3, 7, 3, "https://www.platon.network", sitestyle),
        (8, 3, 11, 3, "https://sg.platon.network", sitestyle),
        (12, 3, 15, 3, "https://www.ont.io", sitestyle),
        (16, 3, 19, 3, "https://www.ethereum.org", sitestyle)
    ]
    merge_cell(worksheet, cells)

    for i in range(4, 7):
        raw = 4
        for j in range(0, 4):
            if i == 4:
                cells = [(raw, 4, "PC网页", commonstyle),
                         (raw + 1, 4, "手机(移动)", commonstyle),
                         (raw + 2, 4, "手机(电信)", commonstyle),
                         (raw + 3, 4, "手机(联通)", commonstyle)]
            else:
                cells = [(raw, i, "", commonstyle),
                         (raw + 1, i, "", commonstyle),
                         (raw + 2, i, "", commonstyle),
                         (raw + 3, i, "", commonstyle)]
            write_cell(worksheet, cells)
            raw += 4


def work_charts(workbook, worksheet, sheet_names, series_names, col, position):
    # 创建一个条形图
    chart1 = workbook.add_chart({"type": "bar"})
    chart1.add_series({
        "name": "%s" % (series_names),
        "categories": "='%s'!$B$3:$B$12" % sheet_names,
        "values": "'%s'!$%s$3:$%s$12" % (sheet_names, col, col),
        "data_labels": {"value": True},
        "line": {"none": True},
    })

    chart1.set_title({"name": "%s的%s" % (sheet_names, series_names)})

    chart1.set_style(27)
    worksheet.insert_chart(position, chart1)


def works():
    dates = datetime.today().strftime("%Y%m%d%H%M")
    filename = u"PlatON网站服务优化监测表-汇总-%s.xlsx" % (dates)
    workbook = xlsxwriter.Workbook(filename=filename)
    titlestyle = workbook.add_format()
    coltitlestyle = workbook.add_format()

    title_style(titlestyle, "#00B0F0", ["center", "vcenter"])
    title_style(coltitlestyle, "#00B0F0", ["center"])

    areaStyle = workbook.add_format()
    set_font(areaStyle, 12, "宋体", 1)

    dataStyle = workbook.add_format()
    set_font(dataStyle, 12, "Arial", 1)

    workchart = workbook.add_worksheet("网站访问监测图表")
    currentcol = 1
    source = Asm()
    for site in sites.keys():
        # 数据写入行号及列数
        row = 2
        # add_worksheet限制名称不能多于32个字符
        worksheet = workbook.add_worksheet("%s数据" % (sites.get(site)))
        # 设置标题所在行行高
        worksheet.set_row(0, 70)
        # 设置第二列宽度为38个字符,设置第三列到第七列宽度为17个字符
        worksheet.set_column(1, 1, 38)
        worksheet.set_column(2, 6, 17)
        # 合并第1行的第2到7列，并写入标题
        worksheet.merge_range(0, 1, 0, 6,
                              "%s网站服务网页监测例检表%s" % (sites.get(site), dates),
                              titlestyle)

        # 在第二行写入表格的列名
        cells = [(1, 1, "地区/国家", coltitlestyle),
                 (1, 2, "访问总时间(s)", coltitlestyle),
                 (1, 3, "解析时间(ms)", coltitlestyle),
                 (1, 4, "连接时间(ms)", coltitlestyle),
                 (1, 5, "下载时间(ms)", coltitlestyle),
                 (1, 6, "访问状态(ms)", coltitlestyle)]
        write_cell(worksheet, cells)
        api = CONFIG.cp_config
        urls = []
        for code in codes:
            url = api + ("?checkloc=%s&type=https&host=%s&path=&port=443&"
                         "callback=update_") % (code, site)
            urls.append(url)
        results = source.get_data(urls)
        print(results)
        for result in results:
            try:
                country, city, rtime, ctime, dtime = result
            except (AsmError, AssertionError):
                continue
            write_cell(worksheet, [(row, 1, "%s-%s" % (
                countryCode.get(country), cityCode.get(city)), areaStyle)])
            cells = [(row, 3, int(rtime), dataStyle),
                     (row, 4, int(ctime), dataStyle),
                     (row, 5, int(dtime), dataStyle)]
            write_number(worksheet, cells)
            worksheet.write_formula(row, 2,
                                    "=SUM(D%s:F%s)/1000" % (row + 1, row + 1),
                                    dataStyle)
            worksheet.write_formula(row, 6,
                                    '=IF(C%s>3,"超时",IF(C%s=0,"超时",IF(C%s>3,"超时","OK")))' % (
                                        row + 1, row + 1, row + 1),
                                    dataStyle)
            row += 1
        column = xl_col_to_name(currentcol)
        for item in [("访问总时间(s)", "C", "%s2" % column),
                     ("解析时间(ms)", "D", "%s20" % column),
                     ("连接时间(ms)", "E", "%s38" % column),
                     ("下载时间(ms)", "F", "%s56" % column)]:
            work_charts(workbook, workchart, worksheet.name, item[0], item[1],
                        item[2])
        currentcol += 10
    create_extra_table(workbook, titlestyle, coltitlestyle)

    workbook.close()
    LOG.info("%s写入数据完成" % filename)
