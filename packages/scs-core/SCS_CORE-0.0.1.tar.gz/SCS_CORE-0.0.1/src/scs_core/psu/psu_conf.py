"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A stub PSUConf
"""


# --------------------------------------------------------------------------------------------------------------------

class PSUConf(object):
    """
    classdocs
    """

    @classmethod
    def models(cls):
        return []


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, _host):
        return cls()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def psu(cls, _host, _interface_model):
        return None


    @classmethod
    def psu_monitor(cls, _host, _interface_model, _auto_shutdown):
        return None


    @classmethod
    def psu_report_class(cls):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return None


    @property
    def report_file(self):
        return None
