import os
import moviepy.editor as mp
import speech_recognition as sr

# Папки
video_folder = 'Unprocessed_video'
output_folder = 'videos'

# Создаем папку для текстовых файлов, если она не существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Инициализация распознавателя речи
recognizer = sr.Recognizer()

# Функция для извлечения текста из аудио
def extract_text_from_audio(audio_path):
    audio = sr.AudioFile(audio_path)
    with audio as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language='ru-RU')
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Error with speech recognition service: {e}")
        return ""

# Обработка каждого видео файла
for video_file in os.listdir(video_folder):
    if video_file.endswith('.mp4'):
        video_path = os.path.join(video_folder, video_file)
        
        # Конвертация видео в аудио
        video = mp.VideoFileClip(video_path)
        audio_path = video_path.replace('.mp4', '.wav')
        video.audio.write_audiofile(audio_path)

        # Извлечение текста из аудио
        text = extract_text_from_audio(audio_path)
        
        # Сохранение текста в файл
        text_file_name = os.path.splitext(video_file)[0] + '.txt'
        text_file_path = os.path.join(output_folder, text_file_name)
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        
        # Удаление временного аудио файла
        os.remove(audio_path)

        print(f"Обработано видео: {video_file}, текст сохранен в: {text_file_path}")

print("Все видео успешно обработаны.")
