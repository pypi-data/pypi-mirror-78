import argparse

from .api_server import ApiServer
from .mq_server import MqServer
from .schedule_server import ScheduleServer


def main():
    parser = argparse.ArgumentParser(description='Describe your program')
    parser.add_argument('-m', '--mode', type=str, default='abc', help='''
        - a 提供api供其它服务调用的方式来操作issue;
        - b 提供MQ消费者的方式来操作issue;
        - c 提供定时任务来操作issue;
    ''')
    args = parser.parse_args()
    print(args)

    # 运行Flask
    ApiServer()

    # 监听RBMQ
    MqServer()

    # 定时任务
    ScheduleServer()


if __name__ == '__main__':
    main()
