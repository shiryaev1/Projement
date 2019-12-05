import xlwt
from django.http import HttpResponse

from projects.models import Project


def export_projects_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="projects.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Projects Data')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        'company',
        'title',
        'start_date',
        'end_date',
        'estimated_design',
        'actual_design',
        'estimated_development',
        'actual_development',
        'estimated_testing',
        'actual_testing',
        'tags',
        'additional_hour_design',
        'additional_hour_development',
        'additional_hour_testing',
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Project.objects.all().values_list(
        'company',
        'title',
        'start_date',
        'end_date',
        'estimated_design',
        'actual_design',
        'estimated_development',
        'actual_development',
        'estimated_testing',
        'actual_testing',
        'tags',
        'additional_hour_design',
        'additional_hour_development',
        'additional_hour_testing',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response