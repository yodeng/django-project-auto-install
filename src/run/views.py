from django.shortcuts import render

# Create your views here.

import os
import json
import textwrap
import requests
import datetime
import subprocess
import logging
import threading

from django.views import View
from django.conf import settings
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

loger = logging.getLogger("django.server")

err = {
    "statucode": 1,
    "msg": "error",
    "analysis_dir": ""
}
suc = {
    "statucode": 0,
    "msg": "success",
    "analysis_dir": ""
}


def text_wrap(text):
    return textwrap.dedent(text)


def run(analysis_dir):
    try:
        samplefile = os.path.join(analysis_dir, "kpipestart.list")
        outdir = os.path.join(analysis_dir, "analysis")
        cmd = "%s -od %s -list %s -para %s && " % (os.path.join(settings.KPIPE, "kpipe"),
                                                   outdir, samplefile, os.path.join(settings.KPIPE, "paramaters.cfg"))
        cmd += "rm -fr %s %s" % (os.path.join(outdir, "mid"),
                                 os.path.join(outdir, "shell"))
        with open(os.path.join(analysis_dir, "run.sh"), "w") as fo:
            fo.write(cmd + "\n")
        subprocess.call("nohup sh " + os.path.join(analysis_dir, "run.sh") + " &> %s/run.log &" %
                        analysis_dir, shell=True)
    except Exception as err:
        loger.error(err.args[0])
        '''
        response error to status recive api if possible
        '''
        raise err


@method_decorator(csrf_exempt, name='dispatch')
class Kpipe(View):

    def get(self, request):
        return Http404()

    def post(self, request):
        analysis_dir = os.path.join(
            settings.KPIPE_PROJ_DIR, datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S-%f"))
        try:
            received_json_data = json.loads(request.body.decode())
            check_kpipe(received_json_data, analysis_dir)
            t = threading.Thread(target=run, args=(analysis_dir, ))
            t.start()
            sucinfo = suc.copy()
            sucinfo["analysis_dir"] = analysis_dir
            return JsonResponse(sucinfo, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            loger.error(e.args[0])
            errinfo = err.copy()
            errinfo["msg"] = e.args[0]
            errinfo["analysis_dir"] = analysis_dir
            return JsonResponse(errinfo, json_dumps_params={'ensure_ascii': False})


def check_file(path):
    assert os.path.isfile(path), "No such file %s" % path


def check_key(k, d, m):
    assert k in d, "'%s' must in %s" % (k, m)


def check_kpipe(data, analysis_dir):
    lines = []
    key_info = "sample info"
    for sn in data["samples"]:
        l = []
        check_key("name", sn, key_info)
        l.append(sn["name"])
        check_key("read_length", sn, key_info)
        l.append(sn["read_length"])
        check_key("fq1_path", sn, key_info)
        check_file(sn["fq1_path"])
        l.append(sn["fq1_path"])
        if "fq2_path" in sn:
            check_file(sn["fq2_path"])
            l.append(sn["fq2_path"])
        lines.append(l)
    if not os.path.isdir(analysis_dir):
        os.makedirs(analysis_dir)
    with open(os.path.join(analysis_dir, "kpipestart.json"), "w") as fo:
        json.dump(data, fo, indent=2)
    with open(os.path.join(analysis_dir, "kpipestart.list"), "w") as fo:
        for l in lines:
            l = map(str, l)
            fo.write("\t".join(l) + "\n")
