import random


class ServerSimulation:
    """
    type_id - int тип заполнения серверов (1 - рандомное, 0 - зеркальное)
    server_amount - int кол-во серверов
    data_amount -  int кол-во кусков данных
    data_chunks - словарь: key - номер сервера, value - список кусков данных
    """
    data_chunks = {}

    def __init__(self, type_id, servers_amount=10, data_amount=100):
        self.servers_amount = servers_amount
        self.data_amount = data_amount
        for i in range(servers_amount):
            self.data_chunks[i] = []
        if type_id:
            self.init_random_placement()
        else:
            self.init_full_copy_placement()

    def init_random_placement(self):
        """
        с помощью random.shuffle() получаем рандомный список кусков данных
        и затем записываем одну копию на первую половину серверов, затем повторяем для
        копии данных и записываем на оставшиеся сервера
        """
        random_data = list(range(0, self.data_amount))
        server_num = 0
        for times in range(2):
            random.shuffle(random_data)
            for i in random_data:
                if len(self.data_chunks[server_num]) < 20:
                    self.data_chunks[server_num].append(i)
                else:
                    server_num += 1
                    self.data_chunks[server_num].append(i)

    def init_full_copy_placement(self):
        """
        с помощью random.shuffle() получаем рандомный список кусков данных
        и затем записываем одну копию на первую половину серверов, затем клонируем их
        """
        random_data = list(range(0, self.data_amount))
        server_num = 0
        random.shuffle(random_data)
        for i in random_data:
            if len(self.data_chunks[server_num]) < 20:
                self.data_chunks[server_num].append(i)
            else:
                server_num += 1
                self.data_chunks[server_num].append(i)
        for key in range(server_num+1):
            self.data_chunks[key+self.servers_amount/2] = self.data_chunks[key]

    def test_servers(self):
        """
        проверяем есть ли в каждых двух серверах один общий кусок данных - если есть относим эту пару к
        тем случаям, когда данные теряются, если нет - к тем, когда не теряется

        итоговый процент = кол-во раз потеряли данные/(кол-во раз не потеряли + кол-во раз потеряли)
        """
        list_keys = list(self.data_chunks.keys())
        lost_data = 0
        not_lost_data = 0
        for i in range(0, len(list_keys)):
            for j in range(i+1, len(list_keys)):
                for data_part in self.data_chunks[i]:
                    if data_part in self.data_chunks[j]:
                        lost_data += 1
                        break
                else:
                    not_lost_data += 1
        return 'Killing 2 arbitrary servers results in data loss in ' + \
               str(round(100*lost_data/(not_lost_data+lost_data), 2)) + '% cases'


ex = ServerSimulation(0)

print(ex.test_servers())
