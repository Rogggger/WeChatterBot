#  coding: utf-8
import os
import psutil
from flask_login import login_required
from flask import Blueprint
import platform
from app.decorator.auth import admin_required
from app.libs.http import jsonify

bp_admin_system = Blueprint('admin_system_info', __name__, url_prefix='/admin/system_info')

CPU_INFO = u'{}'
RAM_INFO = u'{}'
DISK_INFO = u'{}'


@bp_admin_system.route("/", methods=["GET"])
@login_required
@admin_required
def get_sys_info():  # 返回所有当前用户可以审核的条目
    print(platform.platform())
    total_cpu = psutil.cpu_times().user + psutil.cpu_times().idle
    user_cpu = psutil.cpu_times().user
    cpu_syl = user_cpu / total_cpu * 100
    mem = psutil.virtual_memory()
    mem_total = mem.total
    mem_used = mem.used
    mem_syl = mem_used / float(mem_total) * 100
    dis_syl = psutil.disk_usage('/').used / float(psutil.disk_usage('/').total) * 100

    data = {'cpu': CPU_INFO.format(cpu_syl), 'memory': RAM_INFO.format(mem_syl),
            'hard_disk': DISK_INFO.format(dis_syl), 'system': platform.platform()}

    return jsonify(data)


# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def get_ram_info():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return line.split()[1:4]


# Return % of CPU used by user as a character string
def get_cpu_use():
    return str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())


# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def get_disk_space():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return line.split()[1:5]
