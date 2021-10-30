'''
    Create by ChasonJiang(WhiteJiang)
        2021.10.29
'''
import os
import yaml
import requests


class XiaomiRomQuery:
    def __init__(self):
        # fw_yaml_url = "https://xiaomifirmwareupdater.com/data/devices/latest.yml"
        rom_yaml_url = "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/data/latest.yml"
        self.yaml_data = yaml.load(requests.get(rom_yaml_url).text,Loader=yaml.FullLoader)
        self.branch_map={"stable":"Stable","stable beta":"Stable Beta","beta":'Weekly'}
        self.method={"recovery":"Recovery","fastboot":"Fastboot",}
        self.codename={}
        for i in self.yaml_data:
            self.codename[i["codename"]] =""
        self.codename = sorted(list(self.codename.keys()))
        

    def query_rom(self,model_name,region,rom_cleases,rom_version):
        '''
            该函数用于查询miui rom链接
            参数解释：
                model_name:机型代号，如：小米10的代号就是umi
                region：机型地区，cn eea in 等等，必须小写
                rom_cleases：rom类型  recovery或fastboot
                rom_version： 卡刷包（recovery）版本 beta 或 stable  注：线刷包无该选项
        '''
        codename=self.query_codename(model_name,region)
        for item in self.yaml_data:
            if item["codename"] == codename and item["branch"]==self.branch_map[rom_version] and item["method"]==self.method[rom_cleases]:
                return item["link"]

    def query_codename(self,model_name,region):
        for i in self.codename:
            if i == model_name and region=="cn":
               return model_name
        codename = model_name+"_"+region+"_global"
        for i in self.codename:
            if i == codename:
               return codename
        raise RuntimeError("Could not find {}".format(codename))


if __name__=='__main__':
    # step 0: set parameters
    model_name = "umi"
    region = "cn"
    rom_cleases = "recovery"
    rom_version = "stable"
    # step 1: create XiaomiRomQuery object
    xiaomiRomQuery = XiaomiRomQuery()
    # step 2: get rom link by query_rom()
    print(xiaomiRomQuery.query_rom(model_name,region,rom_cleases,rom_version))
