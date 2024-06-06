import os
from pytube import YouTube

# Путь к файлу с ссылками на YouTube видео
links_file = 'links.txt'
# Папка для скачивания видео
download_folder = 'Unprocessed_video'

# Создаем папку для скачивания видео, если она не существует
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Функция для загрузки видео
def download_video(url, download_folder):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        video.download(output_path=download_folder)
        print(f"Видео '{yt.title}' успешно скачано.")
    except Exception as e:
        print(f"Ошибка при скачивании видео по ссылке {url}: {e}")

# Чтение ссылок из файла и загрузка видео
with open(links_file, 'r') as file:
    links = file.readlines()

for link in links:
    link = link.strip()  # Убираем пробелы и символы новой строки
    if link:
        download_video(link, download_folder)

print("Все видео успешно скачаны.")
