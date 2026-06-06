#!/bin/bash

#сайти для перевірки
a=("https://google.com" "https://facebook.com" "https://twitter.com")

#файл логів
b="log.txt"

#очищаємо файл
echo "" > $b

#цикл по сайтах
for i in ${a[@]}
do

  #перевіряємо через curl

  c=$(curl -L -s -o /dev/null -w "%{http_code}" $i)
  if [ $c == 200 ]
  then
    echo "<$i> is UP" >> $b
  else
    echo "<$i> is DOWN" >> $b
  fi

done
echo "Готовий файл: $b"