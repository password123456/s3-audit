__author__ = 'https://github.com/password123456/'

import os
import sys
import importlib
from datetime import datetime
import requests
import urllib3
import subprocess

importlib.reload(sys)

_today_ = datetime.today().strftime('%Y-%m-%d')
_home_path_ = '%s' % os.getcwd()
_domain_list_ = '%s/domain.txt' % _home_path_
_scan_result_logs_ = '%s/output/%s-scanned.log' % (_home_path_, _today_)

_header_ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}


class Bcolors:
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    Endc = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def scan_result_logs(_contents):
    _make_output_dir = '%s/output' % _home_path_
    _mode = 'w'

    if os.path.exists(_make_output_dir):
        if os.path.exists(_scan_result_logs_):
            _mode = 'a'
    else:
        _mode = 'w'
        os.makedirs(_make_output_dir)

    with open(_scan_result_logs_, _mode) as fa:
        fa.write('%s' % _contents)
    fa.close()


def s3_check_list_object(_list, _s3_region):
    _result = ''
    try:
        output = subprocess.check_output('aws s3 ls s3://%s --recursive --region %s --no-sign-request'
                                         % (_list, _s3_region), shell=True, stderr=subprocess.STDOUT)

        output = output.decode('utf-8')
        print(output)
        _result = 'ListObject: True'
    except subprocess.CalledProcessError as e:
        _result = 'ListObject: False'
        #print(e.output)

    return _result


def s3_check_put_object(_list, _s3_region):
    cwd = os.getcwd()
    _result = ''
    try:
        output = subprocess.check_output('aws s3 cp %s/7749.html s3://%s --region %s --no-sign-request'
                                         % (cwd, _list, _s3_region), shell=True, stderr=subprocess.STDOUT)
        output = output.decode('utf-8')
        if 'upload' in output:
            _result = 'PutObject: True'
            print(output)
    except subprocess.CalledProcessError as e:
        _result = 'PutObject: False'
        #print(e.output)

    return _result


def s3_check_delete_object(_list, _s3_region):
    _result = ''
    try:
        output = subprocess.check_output('aws s3 rm s3://%s/7749.html --region %s --no-sign-request'
                                         % (_list, _s3_region), shell=True, stderr=subprocess.STDOUT)
        output = output.decode('utf-8')
        if 'delete' in output:
            _result = 'DeleteObject: True'
            print(output)
    except subprocess.CalledProcessError as e:
        _result = 'DeleteObject: False'
        #print(e.output)

    return _result


def get_list():
    _scan_result = ''
    _not_scan_result = ''

    not_given_result = '[ListObject: Not_Given, PutObject: Not_Given, DeleteObject: Not_Given]'

    try:
        if os.path.exists(_domain_list_):
            with open(_domain_list_, 'r') as f:
                _scan_count = 0
                _not_scan_count = 0
                for line in f:
                    if not len(line.strip()) == 0:
                        _list = line.replace('\n', '')
                        if _list:
                            prefixes = ['http://', 'https://']

                            if not _list.startswith(tuple(prefixes)):
                                _url = 'https://%s' % _list
                            else:
                                _url = _list

                            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                            try:
                                r = requests.get(_url, headers=_header_, allow_redirects=False, verify=False)
                                if 'amazons3' in r.headers.get('Server').lower():
                                    if r.headers.get('x-amz-bucket-region'):
                                        _s3_region = r.headers['x-amz-bucket-region']
                                        _scan_count = _scan_count + 1

                                        _list_scan = s3_check_list_object(_list, _s3_region)
                                        _put_scan = s3_check_put_object(_list, _s3_region)
                                        _delete_scan = s3_check_delete_object(_list, _s3_region)

                                        _scan_result += '%s,%s %s [%s, %s, %s]\n' % (_scan_count, datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                                                                                    _list, _list_scan, _put_scan, _delete_scan)
                                    else:
                                        _not_scan_count = _not_scan_count + 1

                                        _not_scan_result += '%s,%s %s %s\n' % (_not_scan_count, datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                                                                               _list, not_given_result)
                                else:
                                    _not_scan_count = _not_scan_count + 1

                                    _not_scan_result += '%s,%s %s %s\n' % (_not_scan_count, datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                                                                           _list, not_given_result)
                            except KeyboardInterrupt:
                                sys.exit(0)
                            except Exception as e:
                                print('%s- Exception::%s%s' % (Bcolors.Yellow, e, Bcolors.Endc))
                            else:
                                r.close()

                if _scan_count >= 1:
                    _scan_result = '##### Scan Completed ####\n%s\n' % _scan_result
                    scan_result_logs(_scan_result)

                if _not_scan_count >= 1:
                    _not_scan_result = '##### This is not S3(?). Make sure domain is correct. ####\n%s\n' \
                                       % _not_scan_result
                    scan_result_logs(_not_scan_result)
            f.close()

            print('%s' % _scan_result)
            print('%s' % _not_scan_result)

        else:
            print('%s- File not found.! check %s%s' % (Bcolors.Yellow, _domain_list_, Bcolors.Endc))
    except Exception as e:
        print('%s- Exception::%s%s' % (Bcolors.Yellow, e, Bcolors.Endc))


def main():
    get_list()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print('%s- Exception::%s%s' % (Bcolors.Yellow, e, Bcolors.Endc))
