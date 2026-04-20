import socket
import threading
import time
import random
from datetime import datetime

class ThreadedServer:
    """
    Многопоточный эхо-сервер с использованием threading
    """
    
    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_counter = 0
        self.counter_lock = threading.Lock()
        
    def start(self):
        """Запуск сервера"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        
        self._print_banner()
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                
                with self.counter_lock:
                    self.client_counter += 1
                    client_id = self.client_counter
                
                print(f"\n[СЕРВЕР] Новое подключение: клиент #{client_id} с адреса {client_address}")
                
                # Создаем и запускаем поток-обработчик
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address, client_id),
                    name=f"Handler-{client_id}"
                )
                client_thread.start()
                print(f"[СЕРВЕР] Создан поток {client_thread.name} для клиента #{client_id}")
                print(f"[СЕРВЕР] Активных потоков: {threading.active_count() - 1}")
                
        except KeyboardInterrupt:
            print("\n[СЕРВЕР] Получен сигнал завершения работы...")
        finally:
            self.stop()
    
    def _handle_client(self, client_socket, client_address, client_id):
        """
        Обработчик одного клиента (выполняется в отдельном потоке)
        """
        thread_name = threading.current_thread().name
        print(f"[СЕРВЕР] Начало обработки клиента #{client_id} (поток: {thread_name})")
        
        try:
            while True:
                # Получаем данные
                raw_data = client_socket.recv(1024)
                
                if not raw_data:
                    print(f"[СЕРВЕР] Клиент #{client_id} отключился")
                    break
                
                message = raw_data.decode('utf-8').strip()
                print(f"[СЕРВЕР] Клиент #{client_id} отправил: '{message}'")
                
                # Проверка команды выхода
                if message.lower() in ('exit', 'quit'):
                    print(f"[СЕРВЕР] Клиент #{client_id} завершает сеанс")
                    client_socket.send(b"Goodbye! Connection closed.")
                    break
                
                # Имитация "тяжелых" вычислений
                thinking_time = random.uniform(2, 8)
                print(f"[СЕРВЕР] Клиент #{client_id} обрабатывает запрос... "
                      f"(задержка {thinking_time:.1f} сек)")
                time.sleep(thinking_time)
                
                # Модификация сообщения (эхо + верхний регистр + время обработки)
                current_time = datetime.now().strftime("%H:%M:%S")
                modified_message = f"[{current_time}] ECHO ({thread_name}): {message.upper()}"
                
                # Отправка ответа
                client_socket.send(modified_message.encode('utf-8'))
                print(f"[СЕРВЕР] Клиенту #{client_id} отправлен ответ: '{modified_message}'")
                
        except ConnectionResetError:
            print(f"[СЕРВЕР] Клиент #{client_id} неожиданно разорвал соединение")
        except Exception as e:
            print(f"[СЕРВЕР] Ошибка при обработке клиента #{client_id}: {e}")
        finally:
            client_socket.close()
            print(f"[СЕРВЕР] Завершение обработки клиента #{client_id} (поток {thread_name})")
    
    def _print_banner(self):
        """Вывод баннера сервера"""
        print("=" * 60)
        print("МНОГОПОТОЧНЫЙ ЭХО-СЕРВЕР")
        print(f"Адрес: {self.host}:{self.port}")
        print("Режим: Многопоточный (threading)")
        print("Имитация нагрузки: random(2-8) секунд")
        print("=" * 60)
        print("Сервер запущен и ожидает подключений...\n")
    
    def stop(self):
        """Остановка сервера"""
        if self.server_socket:
            self.server_socket.close()
            print("[СЕРВЕР] Сервер остановлен")

def main():
    server = ThreadedServer()
    server.start()

if __name__ == "__main__":
    main()