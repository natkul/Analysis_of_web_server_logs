from collections import Counter
import argparse
import re
import pathlib
import json

parser = argparse.ArgumentParser(description='Log file parser application.')
parser.add_argument('-p', '--path', required=True)
args = parser.parse_args()


def prepare_list_files():
    path = args.path
    if path[-1:] == '/':
        filenames = []
        for filepath in pathlib.Path(path).glob('**/*.log'):
            filenames.append(filepath.absolute())
    elif path[-4:] == '.log':
        filenames = [path]
    else:
        raise Exception('path invalid')
    return filenames


def parse_url(line):
    regexp_url = r'https?:\/\/\S+'
    parsed_result = re.findall(regexp_url, line)
    if parsed_result:
        parsed_result = parsed_result[0][:-1]
    return parsed_result


def parse_ip(line):
    regexp_ip = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    parsed_result = re.findall(regexp_ip, line)[0]
    return parsed_result


def parse_methods(line):
    regexp_methods = r'GET |POST |HEAD |PUT |DELETE |CONNECT |OPTIONS |TRACE |PATCH '
    parsed_result = re.findall(regexp_methods, line)
    if parsed_result:
        parsed_result = parsed_result[0][:-1]
    return parsed_result


def parse_datatime(line):
    regexp_datatime = r'[0-9]{1,2}\d+\/[a-zA-Z]{1,3}\w+\/[0-9]{1,4}\d+\:[0-9]{1,2}\d+\:[0-9]{1,2}\d+\:[0-9]{1,2}\d+'
    parsed_result = re.findall(regexp_datatime, line)[0]
    return parsed_result


def parse_request_duration(line):
    regexp_request_duration = r'\d+$'
    parsed_result = int(re.findall(regexp_request_duration, line)[0])
    return parsed_result


def parse_files(files):
    ar = []
    for file in files:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                ar.append({'ip': parse_ip(line),
                           'method': parse_methods(line),
                           'url': parse_url(line),
                           'datatime': parse_datatime(line),
                           'request_duration': parse_request_duration(line)
                           })

    return ar


def non_sorted_ar():
    files = prepare_list_files()
    return parse_files(files)


def total_number_of_completed_requests():
    return len(non_sorted_ar())


def number_of_requests_by_http_methods():
    not_sorted = non_sorted_ar()
    return Counter([d['method'] for d in not_sorted])


def top_3_ip_addresses():
    not_sorted = non_sorted_ar()
    sort_count = Counter([d['ip'] for d in not_sorted])
    return dict(sort_count.most_common(3))


def top_request_duration():
    not_sorted = non_sorted_ar()
    sorted_array = sorted(not_sorted, key=lambda d: d['request_duration'], reverse=True)
    return sorted_array[:3]


def collect_json():
    data = {}
    data['total_number_of_completed_requests'] = [total_number_of_completed_requests()]
    data['number_of_requests_by_http_methods'] = [number_of_requests_by_http_methods()]
    data['top_3_ip_addresses'] = [top_3_ip_addresses()]
    data['top_request_duration'] = [top_request_duration()]
    with open('statistics.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == '__main__':
    collect_json()
