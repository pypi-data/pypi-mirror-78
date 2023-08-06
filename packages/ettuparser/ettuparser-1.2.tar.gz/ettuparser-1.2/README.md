# ETTUParser

*DISCLAIMER: Корректная работа модуля не гарантируется, так как возможны ~~изменения сайта ETTU~~ второе пришествие и судный день.*

This project parses ETTU(Ekaterinburg Tram and Trolley Administration) site for mass transit schedule. 

Этот проект парсит сайт ЕТТУ(Екатеринбургское трамвайно-троллейбусное управление) на предмет времени до прибытия троллейбуса/трамвая на остановку.

*The documentation for this repository is written in Russian, cause a problem that this project solves is applicable only to Yekaterinburg.*

## Установка
`pip install ettuparser`
## Использование
Данный модуль зависит от `lxml` и `pandas`.

Единственной функцией данного модуля(на данный момент) является `ettuparser.parseStation(stationID)`. Параметр `stationID` можно взять из URL остановки, информацию о которой требуется получить. К примеру: ht<span>tps://</span>mobile.ettu.ru/station/***3431*** ~~(на разных остановках разное количество символов, возможно, зависит от вида транспорта)~~ (неважно). Возвращает данная функция `pandas.DataFrame`.
