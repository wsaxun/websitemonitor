from datetime import datetime

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from monitor.collect.collector import get_data
from monitor.utils.config import CONFIG
from monitor.utils.log import log_init

LOG = log_init(__name__)

codes = CONFIG.codes_config
sites = CONFIG.sites_config
countryCode = CONFIG.country_code_config
cityCode = CONFIG.city_code_config


def create_extra_table(workbook, title_style, col_title_style):
    dates = datetime.today().strftime("%Y-%m-%d")
    worksheet = workbook.add_worksheet("手工监测数据")
    worksheet.merge_range(1, 1, 1, 6, "网站访问-手工监测数据统计", title_style)
    worksheet.set_row(1, 54)
    worksheet.set_column(1, 1, 12)
    worksheet.set_column(2, 2, 17)
    worksheet.set_column(3, 3, 29)
    worksheet.set_column(4, 4, 13)
    worksheet.set_column(5, 5, 18)
    worksheet.set_column(6, 6, 18)

    worksheet.write_string(3, 1, "监测时间", col_title_style)
    worksheet.write_string(3, 2, "监测站点", col_title_style)
    worksheet.write_string(3, 3, "站点网址", col_title_style)
    worksheet.write_string(3, 4, "监测工具", col_title_style)
    worksheet.write_string(3, 5, "首页相应时间(s)", col_title_style)
    worksheet.write_string(3, 6, "网址是否可访问", col_title_style)

    mergeraw = workbook.add_format({"border": 1})
    mergeraw.set_align("center")
    mergeraw.set_align("vcenter")
    mergeraw.set_font_size(12)
    mergeraw.set_font_name("宋体")

    sitestyle = workbook.add_format(
        {"valign": "vcenter", "border": 1, "font_size": 12})
    commonstyle = workbook.add_format({"font_size": 12, "border": 1})

    worksheet.merge_range(4, 1, 19, 1, "%s" % dates, mergeraw)
    worksheet.merge_range(4, 2, 7, 2, "PlatON(京东)", mergeraw)
    worksheet.merge_range(8, 2, 11, 2, "PlatON(东南亚)", mergeraw)
    worksheet.merge_range(12, 2, 15, 2, "ONT本体(东南亚)", mergeraw)
    worksheet.merge_range(16, 2, 19, 2, "Ethereum(以太坊)", mergeraw)
    worksheet.merge_range(4, 3, 7, 3, "https://www.platon.network", sitestyle)
    worksheet.merge_range(8, 3, 11, 3, "https://sg.platon.network", sitestyle)
    worksheet.merge_range(12, 3, 15, 3, "https://www.ont.io", sitestyle)
    worksheet.merge_range(16, 3, 19, 3, "https://www.ethereum.org", sitestyle)

    for i in range(4, 7):
        raw = 4
        for j in range(0, 4):
            if i == 4:
                worksheet.write_string(raw, 4, "PC网页", commonstyle)
                worksheet.write_string(raw + 1, 4, "手机(移动)", commonstyle)
                worksheet.write_string(raw + 2, 4, "手机(电信)", commonstyle)
                worksheet.write_string(raw + 3, 4, "手机(联通)", commonstyle)
            else:
                worksheet.write_string(raw, i, "", commonstyle)
                worksheet.write_string(raw + 1, i, "", commonstyle)
                worksheet.write_string(raw + 2, i, "", commonstyle)
                worksheet.write_string(raw + 3, i, "", commonstyle)
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

    titlestyle.set_bg_color("#00B0F0")
    titlestyle.set_font_name("宋体")
    titlestyle.set_font_size(16)
    titlestyle.set_bold()
    titlestyle.set_top(1)
    titlestyle.set_bottom(1)
    titlestyle.set_right(1)
    titlestyle.set_left(1)
    titlestyle.set_align("center")
    titlestyle.set_align("vcenter")

    coltitlestyle.set_bg_color("#808080")
    coltitlestyle.set_font_name("宋体")
    coltitlestyle.set_font_size(12)
    coltitlestyle.set_bold()
    coltitlestyle.set_bottom(1)
    coltitlestyle.set_top(1)
    coltitlestyle.set_left(1)
    coltitlestyle.set_right(1)
    coltitlestyle.set_align('center')

    areaStyle = workbook.add_format()
    areaStyle.set_font_size(12)
    areaStyle.set_font_name("宋体")
    areaStyle.set_border(1)

    dataStyle = workbook.add_format()
    dataStyle.set_font_name('Arial')
    dataStyle.set_font_size(10)
    dataStyle.set_border(1)

    workchart = workbook.add_worksheet("网站访问监测图表")
    currentcol = 1
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
        worksheet.write_string(1, 1, "地区/国家", coltitlestyle)
        worksheet.write_string(1, 2, "访问总时间(s)", coltitlestyle)
        worksheet.write_string(1, 3, "解析时间(ms)", coltitlestyle)
        worksheet.write_string(1, 4, "连接时间(ms)", coltitlestyle)
        worksheet.write_string(1, 5, "下载时间(ms)", coltitlestyle)
        worksheet.write_string(1, 6, "访问状态(ms)", coltitlestyle)
        for code in codes:
            api = CONFIG.cp_config
            url = api + ("?checkloc=%s&type=https&host=%s&path=&port=443&"
                      "callback=update_") % (code, site)
            country, city, rtime, ctime, dtime = get_data(url, code)
            worksheet.write_string(row, 1, "%s-%s" % (
                countryCode.get(country), cityCode.get(city)), areaStyle)
            worksheet.write_number(row, 3, int(rtime), dataStyle)
            worksheet.write_number(row, 4, int(ctime), dataStyle)
            worksheet.write_number(row, 5, int(dtime), dataStyle)
            worksheet.write_formula(row, 2,
                                    "=SUM(D%s:F%s)/1000" % (row + 1, row + 1),
                                    dataStyle)
            worksheet.write_formula(row, 6,
                                    '=IF(C%s>3,"超时",IF(C%s=0,"超时",IF(C%s>3,"超时","OK")))' % (
                                        row + 1, row + 1, row + 1),
                                    dataStyle)
            row += 1
        column = xl_col_to_name(currentcol)
        work_charts(workbook, workchart, worksheet.name, "访问总时间(s)", "C",
                   "%s2" % column)
        work_charts(workbook, workchart, worksheet.name, "解析时间(ms)", "D",
                   "%s20" % column)
        work_charts(workbook, workchart, worksheet.name, "连接时间(ms)", "E",
                   "%s38" % column)
        work_charts(workbook, workchart, worksheet.name, "下载时间(ms)", "F",
                   "%s56" % column)
        currentcol += 10
    create_extra_table(workbook, titlestyle, coltitlestyle)

    workbook.close()
    LOG.info("%s写入数据完成" % filename)
