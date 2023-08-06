import sys
from urllib import parse

import pandas as pd
import requests

from cqu_cj.config.config import config, Config
from cqu_cj.utils import check_user, log, check_output_path
from cqu_cj.version import __version__


def main():
    check_user()
    session = requests.Session()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "User-Agent": "Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)",
    }
    data = parse.urlencode(
        {
            "username": config['user_info']['username'],
            "password": config['user_info']['password'],
            "submit1.x": 36,
            "submit1.y": 16,
        }
    )

    # Send login form
    session.post("http://oldjw.cqu.edu.cn:8088/login.asp", headers=headers, data=data)

    # Get grades
    page = session.get("http://oldjw.cqu.edu.cn:8088/score/sel_score/sum_score_sel.asp")

    pd.read_html(page.content.decode('gbk'))[1].to_csv(config['output']['path'], index=None, header=None)
    log(f"已成功导出成绩到{config['output']['path']}")


def console_main():
    import argparse
    check_output_path()

    def parse_args() -> argparse.Namespace:
        """Parse the command line arguments for the `cqu cj` binary.

        :return: Namespace with parsed arguments.
        """
        parser = argparse.ArgumentParser(prog="cj", description="第三方 重庆大学 成绩查询", )

        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"CQU_jwc {__version__}",
            help="显示版本号",
        )
        parser.add_argument(
            "-c",
            "--config_path",
            help="查询配置文件路径",
            action="store_true",
        )
        parser.add_argument(
            "-r", "--reset", help="重置配置项", action="store_true",
        )
        parser.add_argument(
            "-u",
            "--username",
            help="学号",
            type=int,
            default=config["user_info"]["username"],
        )
        parser.add_argument(
            "-p",
            "--password",
            help="密码",
            type=str,
            default=config["user_info"]["password"],
        )
        parser.add_argument(
            "-o",
            "--output",
            help="成绩输出路径",
            type=str,
            default=config['output']['path'],
        )

        return parser.parse_args()

    args = parse_args()
    if args.reset:
        Config.reset()
        log("已重置配置文件")
    if args.config_path:
        log(f"配置文件位于{Config.path}\n")
        sys.exit()

    config.dump()

    main()


if __name__ == '__main__':
    check_output_path()
    main()
