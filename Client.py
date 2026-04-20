import socket
import threading
import time

class EchoClient:
    """Клиент для работы с многопоточным сервером"""
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self):
        """Подключение к серверу"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"[КЛИЕНТ] Подключен к {self.host}:{self.port}")
            return True
        except ConnectionRefusedError:
            print("[КЛИЕНТ] ОШИБКА: Сервер не запущен!")
            return False
        except Exception as e:
            print(f"[КЛИЕНТ] Ошибка подключения: {e}")
            return False
    
    def send_message(self, message):
        """Отправка сообщения и получение ответа"""
        if not self.socket:
            return None
        
        try:
            self.socket.send(message.encode('utf-8'))
            print(f"[КЛИЕНТ] Отправлено: '{message}'")
            
            raw_response = self.socket.recv(1024)
            if not raw_response:
                print("[КЛИЕНТ] Сервер разорвал соединение")
                return None
                
            response = raw_response.decode('utf-8')
            print(f"[КЛИЕНТ] Получен ответ: '{response}'")
            return response
            
        except Exception as e:
            print(f"[КЛИЕНТ] Ошибка: {e}")
            return None
    
    def close(self):
        """Закрытие соединения"""
        if self.socket:
            self.socket.close()
            print("[КЛИЕНТ] Соединение закрыто")

def interactive_mode():
    """Интерактивный режим"""
    print("\n" + "="*50)
    print("ИНТЕРАКТИВНЫЙ РЕЖИМ")
    print("="*50)
    
    client = EchoClient()
    
    if not client.connect():
        return
    
    print("\nВведите сообщения для отправки серверу")
    print("Команды: 'exit' или 'quit' - завершить работу\n")
    
    try:
        while True:
            user_input = input("Вы: ")
            
            if user_input.lower() in ('exit', 'quit'):
                client.send_message(user_input)
                break
            elif user_input.strip():
                client.send_message(user_input)
            else:
                print("Введите сообщение или команду")
                
    except KeyboardInterrupt:
        print("\nПрерывание пользователя")
    finally:
        client.close()

def stress_test():
    """Стресс-тест с несколькими клиентами"""
    print("\n" + "="*50)
    print("СТРЕСС-ТЕСТ (5 клиентов одновременно)")
    print("="*50)
    print("Каждый клиент отправит 2 сообщения")
    print("Сервер будет обрабатывать их параллельно\n")
    
    def client_work(client_num):
        """Работа одного клиента в потоке"""
        client = EchoClient()
        
        if not client.connect():
            return
        
        time.sleep(0.5)
        client.send_message(f"Сообщение 1 от клиента {client_num}")
        time.sleep(1)
        client.send_message(f"Сообщение 2 от клиента {client_num}")
        
        client.close()
    
    threads = []
    for i in range(1, 6):
        t = threading.Thread(target=client_work, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(0.3)
    
    for t in threads:
        t.join()
    
    print("\n[ТЕСТ] Все клиенты завершили работу")

def main():
    print("\n" + "="*60)
    print("МНОГОПОТОЧНЫЙ ЭХО-КЛИЕНТ")
    print("="*60)
    
    while True:
        print("\nВыберите режим работы:")
        print("1. Интерактивный режим (один клиент)")
        print("2. Стресс-тест (5 клиентов одновременно)")
        print("3. Выход")
        
        choice = input("\nВаш выбор (1-3): ").strip()
        
        if choice == '1':
            interactive_mode()
        elif choice == '2':
            stress_test()
        elif choice == '3':
            print("До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main()