import os
from pprint import pprint


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''

    def export_to_html(self, fname='output.html'):
        result = '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Позиции продуктов</title>
                </head>
                <body>
                    <table border>
                        <tr>
                            <th>№</th>
                            <th>Название</th>
                            <th>Цена</th>
                            <th>Фасовка</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>
                '''
        if self.data:
            i = 0
            for product in self.data:
                i += 1
                result += f'''
                        <tr>
                            <td>{i}</td>
                            <td>{product[0]}</td>
                            <td>{product[1]}</td>
                            <td>{product[2]}</td>
                            <td>{product[3]}</td>
                            <td>{product[4]}</td>
                        </tr>
                    '''
            result += '''
                        </table>
                    </body>
                    </html>
                    '''
            with open(fname, 'w', encoding='utf-8') as file:
                file.write(result)
            return 'Data exported successfully.'
        else:
            return "There's no data to export."

    def find_text(self, text):
        if self.data:
            i = 0
            self.result = f'№\t{"Наименование":30}{"Цена":10}{"Вес":6}{"Файл":20}{"Цена за кг":15}'
            for product in self.data:
                if text in product[0].lower():
                    i += 1
                    self.result += f'\n{i}\t{product[0]:30}{product[1]:<10}{product[2]:<6}{product[3]:<20}{product[4]:<15}\t'
            return self.result
        else:
            return f"{'No data':^20}"

    def load_prices(self, path=os.curdir):
        '''
                    Сканирует указанный каталог. Ищет файлы со словом price в названии.
                    В файле ищет столбцы с названием товара, ценой и весом.
                    Допустимые названия для столбца с товаром:
                        товар
                        название
                        наименование
                        продукт

                    Допустимые названия для столбца с ценой:
                        розница
                        цена

                    Допустимые названия для столбца с весом (в кг.)
                        вес
                        масса
                        фасовка
        '''
        dirs = os.walk(path)
        for dirpath, dirname, files in dirs:
            if files:
                for file in files:
                    if 'price' in file.lower():
                        with open(dirpath+'/'+file, 'r', encoding='utf-8') as current_file:
                            product_ind, price_ind, weight_ind = self._search_product_price_weight(current_file.readline())
                            while True:
                                data_line = current_file.readline().replace('\n', '')
                                if data_line != '':
                                    data_line = data_line.split(',')
                                    self.data.append((data_line[product_ind].capitalize(),
                                                      int(data_line[price_ind]),
                                                      int(data_line[weight_ind]),
                                                      file,
                                                      round(int(data_line[price_ind])/int(data_line[weight_ind]), 2)))
                                else:
                                    break
        self.data.sort(key=lambda x: x[-1])
        # раскомментировать строчку ниже, если нужно, чтобы список был отсортирован по названию и цене по возрастанию
        #self.data.sort(key=lambda x: x[0])
        if self.data:
            return 'Data loaded successfully'
        else:
            return "There's no data to load"

    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''

        product_ind, price_ind, weight_ind = None, None, None
        headers = headers.replace('\n', '').split(',')
        for header in headers:
            if header in ('название', 'продукт', 'товар', 'наименование'):
                product_ind = headers.index(header)
            elif header in ('цена', 'розница'):
                price_ind = headers.index(header)
            elif header in ('фасовка', 'масса', 'вес'):
                weight_ind = headers.index(header)

        return product_ind, price_ind, weight_ind


pm = PriceMachine()
print(pm.load_prices())


while True:
    user_input = input('Введите слово, чтобы найти товар.\nЧтобы выйти, напишите exit.\n')
    if user_input == 'exit':
        break
    print(pm.find_text(user_input))

print('the end')
print(pm.export_to_html())
