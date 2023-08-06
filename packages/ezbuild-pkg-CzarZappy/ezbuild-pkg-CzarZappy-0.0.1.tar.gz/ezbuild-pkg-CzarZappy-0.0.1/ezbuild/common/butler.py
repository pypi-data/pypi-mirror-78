from ezbuild.common import bash


def push(org_name: str, project_name: str, output_dir: str, channel_name: str):
    args = ["time", "butler", "push", output_dir,
            '{}/{}:{}'.format(org_name, project_name, channel_name)]
    out = bash.run(args)
    print(out)


def status(org_name: str, project_name: str, channel_name: str):
    args = ["butler", "status", '{}/{}:{}'.format(org_name, project_name, channel_name)]
    out = bash.run(args)
    print(out)
