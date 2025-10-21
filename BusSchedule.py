#BusSchedule.py
#Name:Nola Nelson
#Date:10/21/25
#Assignment:Homework 2

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

def getHours(time):
  """
  Take a time in the format "HH:MM A< and return hour in 24-hour format"
  """
  i = 0
  while i < len(time) and time[i] == " ":
    i = i + 1
  hr_part = ""
  while i < len(time) and time[i] >= "0" and time[i] <= "9":
    hr_part = hr_part + time[i]
    i = i + 1
  if hr_part == "":
    return 0
  
  hour = int(hr_part)

  if "PM" in time and hour < 12:
    hour = hour + 12
  if "AM" in time and hour == 12:
    hour = 0
  return hour

def getMinutes(time):
  i = 0
  while i < len(time) and time[i] == " ":
    i = i + 1
  while i < len(time) and time[i] != ":":
    i = i + 1
  i = i + 1
  
  min_part = ""
  while i < len(time) and time[i] >= "0" and time [i] <= "9":
    min_part = min_part + time[i]
    i = i + 1

  if min_part == "":
    return 0
  minute = int(min_part)
  return minute

def isLater(hr1, min1, hr2, min2):
  if hr1 > hr2:
    return True
  elif hr1 == hr2 and min1 > min2:
    return True
  else:
    return False
  
def getBusTimes(text):
  word = ""
  times = []
  i = 0

  while i < len(text):
    ch = text[i]
    if ch >= "0" and ch <= "9" or ch == ":" or ch == "A" or ch == "P" or ch == "M":
      word = word + ch
    else:
      if ":" in word and ("AM" in word or "PM" in word):
        times.append(word)
      word = ""
    i = i + 1

  if ":" in word and ("AM" in word or "PM" in word):
      times.append(word)
  return times

def main():
  stopNumber = "2269"
  routeNumber = "11"
  direction = "EAST"
  url = "https://myride.ometro.com/Schedule?stopCode=" + stopNumber + "&routeNumber=" + routeNumber + "&directionName=" + direction
  #c1 = loadURL(url) #loads the web page
  c1 = loadTestPage() #loads the test page

  busTimes = getBusTimes(c1)
  
  now = datetime.datetime.now()
  currentHour = (now.hour - 5) % 24
  currentMinute = now.minute

  hourNow = currentHour
  periodNow = "AM"
  if hourNow >= 12:
    periodNow = "PM"
  if hourNow > 12:
    hourNow = hourNow - 12
  if hourNow == 0:
    hourNow = 12

  if currentMinute < 10:
    print("The current time is: ", hourNow, ":0", currentMinute, periodNow)
  else:
    print("The current time is: ", hourNow, ":", currentMinute, periodNow)

  nextBus1 = ""
  nextBus2 = ""
  nextBusCount = 0
  i = 0
  while i < len(busTimes) and nextBusCount < 2:
    h = getHours(busTimes[i])
    m = getMinutes(busTimes[i])
    if isLater(h, m, currentHour, currentMinute):
      if nextBusCount == 0:
        nextBus1 = busTimes[i]
      elif nextBusCount == 1:
        nextBus2 = busTimes[i]
      nextBusCount = nextBusCount + 1
    i = i + 1
  if nextBus1 == "":
    print("There are no more buses today.")
  else:
    minUntilNextBus = (getHours(nextBus1) * 60 + getMinutes(nextBus1)) - (currentHour * 60 + currentMinute)
    if minUntilNextBus < 0:
      minUntilNextBus = minUntilNextBus + 24 * 60
    print("The next bus will arrive in", minUntilNextBus, "minutes.")
  if nextBus2 == "":
    print("There are no more buses after that.")
  else:
    minUntilFollowingBus = (getHours(nextBus2) * 60 + getMinutes(nextBus2)) - (currentHour * 60 + currentMinute)
    if minUntilFollowingBus < 0:
      minUntilFollowingBus = minUntilFollowingBus + 24 * 60
    print("The following bus will arrive in", minUntilFollowingBus, "minutes.")

main()
