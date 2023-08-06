#!/usr/bin/python

from staros.connection import _getsshdata
from staros.connection import _getsshdata3
from staros.connection import _getsshdata1
from staros.connection import _getsshdata2
import staros.connection
import staros.outputparsing
import staros.threadingfind
import datetime
import json


class StarClient:
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def get_subs_msisdn(self, msisdn):
        data = _getsshdata3(self.host, self.port, self.username, self.password, "show subscribers msisdn " + msisdn+"\n")
        return staros.outputparsing._getsubscribermsisdn(str(data))

    def get_subs_session_main(self):
        data = _getsshdata1(self.host, self.port, self.username, self.password, "show subscribers summary\n")
        return staros.outputparsing._parseshowsess(str(data))

    def get_subs_full_imsi(self,imsi):
        data = _getsshdata(self.host, self.port, self.username, self.password, "show subscribers msisdn " + imsi + "\n")

    def get_enodeb_associat_num(self):
        data = _getsshdata2(self.host, self.port, self.username, self.password, "show mme-service enodeb-association summary\n")
        return staros.outputparsing._parseEnodebAssoc(str(data))

    def clear_subs_msisdn(self, msisdn):
        data = _getsshdata1(self.host, self.port, self.username, self.password, "clear subscribers msisdn "+msisdn+" -noconfirm\n")
        return staros.outputparsing._parseClearSubsc(str(data))

    def clear_subs_imsi(self, imsi):
        data = _getsshdata1(self.host, self.port, self.username, self.password, "clear subscribers imsi "+imsi+" -noconfirm\n")
        return staros.outputparsing._parseClearSubsc(str(data))

    def get_device_info(self):
        data = _getsshdata2(self.host, self.port, self.username, self.password, "show version\n")
        return staros.outputparsing._parse_device_info(str(data))

    def get_subs_full_msisdn(self,msisdn):
        data = _getsshdata3(self.host, self.port, self.username, self.password, "show subscribers full msisdn " + msisdn + "\n")
        try:
            staros.outputparsing._get_full_subs_sess_info(str(data))
        except:
            return "Subscriber offline"
        #print data

    def clear_dns_cache_all_Gn(self):
        data = staros.connection._getsshdata4dnsClearContextGn(self.host, self.port, self.username, self.password)
        ddd = staros.outputparsing._clear_dns_gn_parse(data)
        if ddd == True:
            return "DNS cache cleared successful"
        else:
            return "Failed"

    def find_subs_core_list(self, msisdn, ggsnlist):
        ooo = staros.threadingfind.find2(self.port, self.username, self.password, msisdn, ggsnlist)
        return ooo

    def find_subs_core_list_imsi(self, imsi, ggsnlist):
        start = datetime.datetime.now()
        ooo = staros.threadingfind.find2imsi(self.port, self.username, self.password, imsi, ggsnlist)
        end = datetime.datetime.now()
        res = end-start
        ooo.update({"seconds": res.total_seconds()})
        return ooo

    def get_mme_enodeb_list(self, excelpath, page, outputfile):
        staros.threadingfind.getenodeblist(self.host, self.port, self.username, self.password, excelpath, page, outputfile)

    def get_mme_enodeb_list2(self, excelpath, page, outputfile, lastsheet):
        staros.threadingfind.getenodeblist2(self.host, self.port, self.username, self.password, excelpath, page, outputfile, lastsheet)

    def ping_s1u_from_s11(self, sgwlistoam, exelpath, tac):
        staros.threadingfind.ping_s1u_from_s11(self.host, self.port, self.username, self.password, sgwlistoam, exelpath, tac)




