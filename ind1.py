#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Выполнить индивидуальное задание лабораторной работы 4.5, использовав
классы данных, а также загрузку и сохранение данных в формат XML.
"""

from dataclasses import dataclass, field
from datetime import datetime
import sys
from typing import List
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class Routes:
    destination: str
    number: int
    time: str


@dataclass
class Way:
    routes: List[Routes] = field(default_factory=lambda: [])

    def add(self, destination: str, number: int, time: str):

        self.routes.append(
            Routes(
                destination=destination,
                number=number,
                time=time
            )
        )

        self.routes.sort(key=lambda route: route.destination)

    def __str__(self):
        # Заголовок таблицы.
        table = []
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 4,
            '-' * 20
        )
        table.append(line)
        table.append(
            '| {:^30} | {:^4} | {:^20} |'.format(
                "Пункт назначения",
                "№",
                "Время"
            )
        )
        table.append(line)
        # Вывести данные о всех сотрудниках.
        for route in self.routes:
            table.append(
                '| {:<30} | {:>4} | {:<20} |'.format(
                    route.destination,
                    route.number,
                    route.time
                )
            )
        table.append(line)
        return '\n'.join(table)

    def select(self, period: str) -> List[Routes]:
        result: List[Routes] = []

        for route in self.routes:
            time_route = route.time
            time_route1 = datetime.strptime(time_route, "%H:%M")
            time_select = datetime.strptime(period, "%H:%M")
            if time_select < time_route1:
                result.append(route)

        # Возвратить список выбранных маршрутов.
        return result

    def load(self, filename: str) -> None:
        with open(filename, 'r', encoding='utf8') as fin:
            xml = fin.read()

        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)

        self.routes = []
        for route_element in tree:
            destination, number, time = None, None, None

            for element in route_element:
                if element.tag == 'destination':
                    destination = element.text
                elif element.tag == 'number':
                    number = int(element.text)
                elif element.tag == 'time':
                    time = element.text

                if destination is not None and number is not None \
                        and time is not None:
                    self.routes.append(
                        Routes(
                            destination=destination,
                            number=number,
                            time=time
                        )
                    )

    def save(self, filename: str):
        root = ET.Element('workers')
        for route in self.routes:
            route_element = ET.Element('route')

            destination = ET.SubElement(route_element, 'destination')
            destination.text = route.destination

            number_element = ET.SubElement(route_element, 'number')
            number_element.text = str(route.number)

            time_element = ET.SubElement(route_element, 'time')
            time_element.text = route.time

            root.append(route_element)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as f:
            tree.write(f, encoding='utf8', xml_declaration=True)


if __name__ == '__main__':
    # Список маршрутов.
    way = Way()
    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()
        # Выполнить действие в соответствие с командой.

        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о маршруте.
            destination = input("Направление? ")
            number = int(input("Номер? "))
            time = input("Время? ")
            # Добавить маршрут.
            way.add(destination, number, time)

        elif command == 'list':
            # Вывести список.
            print(way)

        elif command.startswith('select '):
            # Разбить команду на части для выделения времени.
            parts = command.split(maxsplit=1)
            # Запросить маршруты.
            selected = way.select(parts[1])
            # Вывести результаты запроса.
            if selected:
                for idx, route in enumerate(selected, 1):
                    print(
                        '{:>4}: {}'.format(idx, route.destination)
                    )
            else:
                print("Маршруты не найдены.")

        elif command.startswith('load '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Загрузить данные из файла.
            way.load(parts[1])

        elif command.startswith('save '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Сохранить данные в файл.
            way.save(parts[1])

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить мавшрут;")
            print("list - вывести список маршрутов;")
            print("select <время> - маршруты после указанного времени;")
            print("load <имя_файла> - загрузить данные из файла;")
            print("save <имя_файла> - сохранить данные в файл;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)
