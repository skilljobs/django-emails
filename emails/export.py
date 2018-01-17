from django.http import StreamingHttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.utils import formats
import csv
import itertools


User = get_user_model()


class Buffer(object):
    """ File-like interface
    """
    def write(self, value):
        return value


def stream_csv_out(qs, headers, row_export_func, file_name='export'):
    """ Stream a large queryset as a CSV response

    :param qs: queryset to stream out
    :param headers: list of CSV headers
    :param row_export_func: returns a list of data attrs to export per object/qdict
    :param file_name: a filename this CSV will download as

    :return: a streaming response with CSV data that will save as a download
    """
    pseudo_buffer = Buffer()
    writer = csv.writer(pseudo_buffer)
    generate_rows = (writer.writerow(row_export_func(u)) for u in qs.iterator())
    rows_with_header = itertools.chain(writer.writerow(headers), generate_rows)

    response = StreamingHttpResponse(rows_with_header, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % file_name
    return response


def export_emails(filters, file_name='export-email'):
    qs = User.objects.filter(**filters).order_by('-id')

    headers = ['User ID', 'Date joined',
               'Email Address', 'First Name', 'Last Name']

    def row_export_func(u):
        return [u.id, formats.date_format(u.date_joined, "SHORT_DATETIME_FORMAT"),
                u.email, u.first_name, u.last_name]

    return stream_csv_out(qs, headers, row_export_func, file_name=file_name)


@staff_member_required
def email_export(request, filters={}):
    return export_emails(filters)
