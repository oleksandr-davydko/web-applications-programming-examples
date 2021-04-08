import socket
import select

HOST = 'localhost'
PORT = 8080
BACKLOG_SIZE = 10
SELECT_TIMEOUT = None   # None для нескінченного циклу в select
RECEIVE_BUFF_SIZE = 1024    # bytes


# Функція для обробки запиту
def work(payload: bytearray) -> bytearray:
    return payload


def main():
    # Створення та конфігурація серверного сокету
    serverSocket = socket.socket()
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(BACKLOG_SIZE)

    """
    Ініціалізація списків для Select
    readList та exceptionalList містять serverSocket, для відслідковування помилок та моментів підключення нових клієнтів
    """
    readList = [serverSocket]
    writeList = []
    exceptionalList = [serverSocket]

    # Ініціалізація контейнера для відповідей
    responsesMap = {}
    # Головний цикл додатку
    while True:
        # Виконуємо select для отримання змін в відслідковуваних сокетах
        readChanges, writeChanges, exceptionalChanges = select.select(readList, writeList, exceptionalList, SELECT_TIMEOUT)
        """
        Створюємо списки для виключення відслідковуваних подій
        Вони нам необхідні для того щоб при виконання наступного select ми обробляти лише очікуємі події від клієнтів
        """
        # Обробляємо сокети які готові для вичитування інформації
        for rSocket in readChanges:
            """
            Перевіряємо чи сокет що згенерував подію не є серверним.
            Подію готовності на цих сокетах необхідно обробити по різному.
            Для серверного необхіжно прийняти клієнта
            Для клієнтського необхідно вичитати дані з сокета
            """
            if rSocket is serverSocket:
                # Приймаємо підключення від клієнта
                client, _ = rSocket.accept()
                # Поміщаємо клієнт в список сокетів що очікують приходу даних
                readList.append(client)
                exceptionalList.append(client)
            else:
                payload = rSocket.recv(RECEIVE_BUFF_SIZE)
                """
                Перевіряємо чи ми отримали повідомлення повністю від клієнта.
                    Якщо так то можемо приступати до обробки запиту
                    Якщо ні, то очікуємо ще даних,
                """
                if payload is not None:
                    # Дані прийшли повнюстю, помічаємо сокет під видалення з цього списку
                    readList.remove(rSocket)
                    # Обробляємо запит
                    response = work(payload)
                    # Зберігаємо результат запиту, щоб повернути для клієнта
                    responsesMap[rSocket] = response
                    # Поміщаємо сокет в список для перевірки на можливість запису
                    writeList.append(rSocket)

        # Обробляємо сокети які готові до запису інформації
        for wSocket in writeChanges:
            # Отримання збереженої відповіді для коієнта
            response = responsesMap.get(wSocket)
            if response is not None:
                # Відправляємо відповідь клієнту
                wSocket.send(response)
                # Очищаємо структури з інформацією про клієнта
                responsesMap.pop(wSocket)
                writeList.remove(wSocket)
                exceptionalList.remove(wSocket)
                # Закриваємо клієнтський сокет
                wSocket.close()

        # Обробляємо сокети що згенерували "exceptional condition"
        for eSocket in exceptionalChanges:
            # Видаляємо сокет з очікуючих на читання
            if eSocket in readList:
                readList.pop(eSocket)
            # Видаляємо відповідь згенеровану для сокету
            if eSocket in writeList:
                responsesMap.pop(eSocket)
                writeList.remove(eSocket)
            """
            Якщо сокет що згенерував викоючення є серверним то ми можемо завершити роботу процесу
            Якщо ні, то нас більше не цікавить інформація про нього
            """
            if eSocket is serverSocket:
                break
            else:
                exceptionalList.remove(eSocket)


if __name__ == '__main__':
    main()


