from zbuild.common import bash


class SteamCMD:

    def __init__(self):
        self.account = "zmaldonado_RHG"
        self.password = "GsucJE737at6"

        # self.account = "panic_state"
        # self.password = "alphadog"

    def login(self):
        args = ["steamcmd", "+login", self.account, self.password, "+quit"]
        out = bash.run(args)
        print(out)

    def run_app_build(self, path):
        args = ["steamcmd", "+login", self.account, self.password, "+run_app_build", path, "+quit"]
        out = bash.run(args)
        print(out)

    def workshop_build_item(self, path):
        args = ["steamcmd", "+login", self.account, self.password, "+workshop_build_item", path, "+quit"]
        out = bash.run(args)
        print(out)

    def app_status(self, app_id):
        args = ["steamcmd", "+login", self.account, self.password, "+app_status", app_id, "+quit"]
        out = bash.run(args)
        print(out)

    def app_info_print(self, app_id):
        args = ["steamcmd", "+login", self.account, self.password, "+app_info_print", app_id, "+quit"]
        out = bash.run(args)
        print(out)

    def app_config_print(self, app_id):
        args = ["steamcmd", "+login", self.account, self.password, "+app_config_print", app_id, "+quit"]
        out = bash.run(args)
        print(out)

    def set_steam_guard_code(self, guard_code):
        args = ["steamcmd", "+set_steam_guard_code", guard_code, "+quit"]
        out = bash.run(args)
        print(out)

