import speedtest
import settings
from lib.common import size_scale
from lib.speedtest_result import SpeedtestResult

if __name__ == '__main__':
    print('fetching last result...')
    last_one = SpeedtestResult.get_last()
    print(last_one)

    s = speedtest.Speedtest()
    s.get_servers([settings.SERVER_ID])

    print('download test... ', end='')
    s.download()
    print(size_scale(s.results.download) + '/s')
    print('upload test... ', end='')
    s.upload()
    print(size_scale(s.results.upload) + '/s')
    print('ping...', s.results.ping, 'ms')
    s.results.share()

    # print(s.results.dict())
    print('storing results...')
    result = SpeedtestResult(s)
    result.save()

    if last_one is not None:
        up_diff = result.upload - last_one.upload
        dn_diff = result.download - last_one.download
        print('download diff: {}{} ({:.2f}%)'.format(
            ['', '+'][dn_diff >= 0],
            size_scale(dn_diff),
            (dn_diff / s.results.download)*100)
        )
        print('upload diff: {}{} ({:.2f}%)'.format(
            ['', '+'][up_diff >= 0],
            size_scale(up_diff),
            (up_diff / s.results.upload)*100)
        )
