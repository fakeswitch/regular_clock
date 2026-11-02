"""SSD1309 demo (flip)."""
from time import sleep
from machine import Pin, SPI,  I2C  # type: ignore
from xglcd_font import XglcdFont
from ssd1309 import Display
import time
import urtc
import senseair_s8


i2c = I2C(1, scl=Pin(7), sda=Pin(6))
rtc = urtc.DS3231(i2c)

s8 = senseair_s8.SenseairS8(uart=1, tx = 4, rx = 5)

# Set the current time using a specified time tuple
# Time tuple: (year, month, day, day of week, hour, minute, seconds, milliseconds)
#initial_time = (2024, 1, 30, 1, 12, 30, 0, 0)

# Or get the local time from the system
#initial_time_tuple = time.localtime()  # tuple (microPython)
#initial_time_seconds = time.mktime(initial_time_tuple)  # local time in seconds

# Convert to tuple compatible with the library
#initial_time = urtc.seconds2tuple(initial_time_seconds)

# Sync the RTC
#rtc.datetime(initial_time)




def format_time(h, m):
    if int(h) >12 : 
        ah = h -12
    elif int(h) == 0:
        ah = str(12)
    else:
        ah = str(h)
    #if int(ah) < 10 : ah = "0" + str(ah)
    if int(m) < 10 : 
        am = "0"+ str(m)
    else:
        am = str(m)
    if int(h) >12: 
        am = am + " PM"
    else: 
        am = am + " AM"
    return str(ah) + ":" + str(am)


def c_to_f(c):
    return ((c*9)/5) +32 

#128 x 64
spi = SPI(1, baudrate=10000000, sck=Pin(10), mosi=Pin(11))
# Initialize display flipped 180 degrees
display = Display(spi, dc=Pin(15), cs=Pin(13), rst=Pin(14), flip=True)

print("Loading font.  Please wait.")

pp2332 = XglcdFont('fonts/PerfectPixel_23x32.c', 23, 32)
roboto = XglcdFont('fonts/Roboto_18x22.c', 18, 22)
wendy = XglcdFont('fonts/Wendy7x8.c', 7, 8)
pp1825 = XglcdFont('fonts/PerfectPixel_18x25.c', 18, 25)
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


#formatted_datetime = (f"{days_of_week[current_datetime.weekday]}, "f"{current_datetime.year:04d}-{current_datetime.month:02d}-{current_datetime.day:02d} ")

hold_time = rtc.datetime()
hold_time = format_time(hold_time.hour, hold_time.minute -1)
hold_temp = temperature = c_to_f(rtc.get_temperature())
hold_co2 = 0
while True:
    current_datetime = rtc.datetime()
    temperature = c_to_f(rtc.get_temperature())
    ftime = format_time(current_datetime.hour, current_datetime.minute)
    day_date = (f"{days_of_week[current_datetime.weekday]}, "f"{current_datetime.year:04d}-{current_datetime.month:02d}-{current_datetime.day:02d} ")
    current_co2 = s8.co2()

    #text_width = wendy.measure_text("Wendy")
    if hold_time != ftime or hold_temp != temperature or current_co2 != hold_co2:
        display.clear_buffers()
        text_width = pp2332.measure_text(ftime)
        display.draw_text((128-text_width)//2 , 0,ftime, pp2332)
        text_width = wendy.measure_text(day_date)
        display.draw_text((128-text_width)//2, 25,day_date, wendy)
        temp_width = pp1825.measure_text(str(round(temperature,1)))
        display.draw_text((64-temp_width)//2, 34,str(round(temperature,1)), pp1825)
        co2_width = pp1825.measure_text(str(round(current_co2,1)))
        display.draw_text(((64-co2_width)//2)+64, 34,str(round(current_co2,1)), pp1825)
        f_width =wendy.measure_text("Fahrenheit") 
        display.draw_text((64-f_width)//2, 56,"Fahrenheit", wendy)
        ct_width = wendy.measure_text("CO2 PPM") 
        display.draw_text((64-ct_width)//2+64, 56,"CO2 PPM", wendy)
        display.present()
        hold_time = ftime
        hold_temp = temperature
        hold_co2 = current_co2
        print( hold_temp, hold_time)
    sleep(5)
