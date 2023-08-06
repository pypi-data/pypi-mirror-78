import sys

from ezbuild.common.steamcmd import SteamCMD


def main(argv):
    print("")

    steam_cmd = SteamCMD()

    workshop_item_path = "/Users/zmaldonado/Projects/Noho/Builds/steam/workshop-demo.vdf"

    steam_cmd.workshop_build_item(workshop_item_path)

    # app_id = "1305520"
    # steam_cmd.app_status(app_id)
    # steam_cmd.app_config_print(app_id)
    # steam_cmd.app_info_print(app_id)


if __name__ == "__main__":
    print('[PUBLISH-WORKSHOP] Number of arguments:', len(sys.argv), 'arguments.')
    print('[PUBLISH-WORKSHOP] Argument List:', str(sys.argv))
    main(sys.argv[1:])
