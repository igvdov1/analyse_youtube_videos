import openai
import os
import json
import time

# Установите ваш API-ключ
api_key = 'Мой Апи ключ'

# Загрузка конфигурационного файла
with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

# Функция для анализа видео
def analyze_videos(api_key, video_dir, config, model="gpt-4"):
    openai.api_key = api_key

    accepted_dir = 'accepted'
    unaccepted_dir = 'unaccepted'
    os.makedirs(accepted_dir, exist_ok=True)
    os.makedirs(unaccepted_dir, exist_ok=True)

    # Определение следующего номера для видео в папке accepted
    existing_accepted_files = [f for f in os.listdir(accepted_dir) if f.startswith("video") and f.endswith(".txt")]
    next_accepted_num = len(existing_accepted_files) + 1

    # Определение следующего номера для видео в папке unaccepted
    existing_unaccepted_files = [f for f in os.listdir(unaccepted_dir) if f.startswith("video") and f.endswith(".txt")]
    next_unaccepted_num = len(existing_unaccepted_files) + 1

    video_files = [f for f in os.listdir(video_dir) if f.endswith('.txt')]

    for i, video_file in enumerate(video_files):
        video_path = os.path.join(video_dir, video_file)
        with open(video_path, 'r', encoding='utf-8') as file:
            video_text = file.read()

        prompt = f"""
Видео: {video_text}
Боли: {', '.join(config['painPoints'])}
Описание ЦА: {config['customerDescription']}
Ожидаемые результаты: {config['expectedResults']}
Критерии отбора: {', '.join(config['criteria'].values())}

Опишите, какие боли из перечисленных решает данное видео и почему. Также укажите, подходит ли видео для молодых мам после родов, и удовлетворяет ли оно всем критериям отбора. Если вы не уверены в контексте видео или вам не хватает данных, отметьте это видео как непригодное для молодых мам. Если видео частично соответствует критериям, отметьте его как пригодное.
"""

        response = None
        max_retries = 5
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an expert assistant helping to analyze video content."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )
                break  # If the request is successful, exit the loop
            except openai.error.APIError as e:
                print(f"APIError: {e} - Attempt {attempt + 1} of {max_retries}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise

        if response is None:
            print(f"Failed to process video {i+1} after {max_retries} attempts.")
            continue

        result = response.choices[0].message['content'].strip()

        print(f"Результат для видео {i+1}: {result}\n")

        if "непригодное" in result.lower() or "не подходит" in result.lower() or "неудовлетворяет" in result.lower():
            dir_path = os.path.join(unaccepted_dir, f"video{next_unaccepted_num}")
            next_unaccepted_num += 1
        else:
            dir_path = os.path.join(accepted_dir, f"video{next_accepted_num}")
            next_accepted_num += 1

        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, video_file), 'w', encoding='utf-8') as f:
            f.write(video_text)
        with open(os.path.join(dir_path, 'resume.txt'), 'w', encoding='utf-8') as f:
            f.write(result)

        print(f"Видео {i+1} обработано.\n")

    print("Анализ завершен. Результаты сохранены в папках accepted и unaccepted.")

# Запуск анализа видео
analyze_videos(api_key, './videos', config)