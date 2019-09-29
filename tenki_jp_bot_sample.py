from tenki_jp_bot import *

def print_forcasts(data):
    print('| time | 天気 | temp'🌤)
    for h in range(24):
        time = str(h + 1).rjust(2) + ':00'
        wthr = data.weather[h].rjust(2, '　')
        temp = data.temperature[h]
        humd = data.humidity[h].rjust(3)
        prec = data.precip[h].rjust(3)
        prec_prob = data.precip_prob[h].rjust(3)
        wind_sped = data.wind_speed[h].rjust(3)
        wind_dirc = data.wind_direc[h].center(3, '　')
        print('| %s | %s | %s | %s | %s | %s | %s | %s |'\
                % (time, wthr, temp, humd, prec, prec_prob, wind_sped, wind_dirc)) 

adress = '7330025'
bot = OneHourForcast()
bot.fetch(adress)
print('Was successful? > %s' % ('Yes' if bot.successful else 'No'))
print('Today\'s forcasts...')
print_forcasts(bot.today)
