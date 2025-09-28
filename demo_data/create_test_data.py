import json
from pathlib import Path

def create_test_json_files():
    base_dir = Path(__file__).parent
    json_dir = base_dir / "json"
    json_dir.mkdir(exist_ok=True)
    
    test_data = {
        "flowers.json": {
            "1": {"pk": 1, "title": "Розы", "color": "красный"},
            "2": {"pk": 2, "title": "Тюльпаны", "color": "розовый"},
            "3": {"pk": 3, "title": "Лилии", "color": "белый"},
            "4": {"pk": 4, "title": "Хризантемы", "color": "желтый"},
            "5": {"pk": 5, "title": "Пионы", "color": "розовый"},
            "6": {"pk": 6, "title": "Орхидеи", "color": "фиолетовый"},
            "7": {"pk": 7, "title": "Герберы", "color": "оранжевый"},
            "8": {"pk": 8, "title": "Ирисы", "color": "синий"}
        },
        "bouquets.json": {
            "1": {
                "pk": 1,
                "title": "Нежность",
                "price": 2500,
                "budget_category": "~2000",
                "image": "static/images/bouquet1.jpg",
                "occasion": "день рождения",
                "meaning": "Этот букет несет в себе всю нежность ваших чувств и не способен оставить равнодушным ни одного сердца!",
                "flowers": [1, 2, 3],
                "color_scheme": "розовый"
            },
            "2": {
                "pk": 2,
                "title": "Элегантность",
                "price": 3200,
                "budget_category": "больше",
                "image": "static/images/bouquet2.jpg",
                "occasion": "свадьба",
                "meaning": "Идеальное сочетание для самого важного дня в вашей жизни - символ чистоты и вечной любви!",
                "flowers": [3, 6, 8],
                "color_scheme": "белый"
            },
            "3": {
                "pk": 3,
                "title": "Радость",
                "price": 1800,
                "budget_category": "~2000",
                "image": "static/images/bouquet3.jpg",
                "occasion": "без повода",
                "meaning": "Простой способ сказать: 'Я думаю о тебе!' - букет, который дарит улыбку!",
                "flowers": [4, 7],
                "color_scheme": "желтый"
            },
            "4": {
                "pk": 4,
                "title": "Романтика",
                "price": 1100,
                "budget_category": "~1000",
                "image": "static/images/bouquet4.jpg",
                "occasion": "14 февраля",
                "meaning": "Классика любви - красные розы, которые говорят о страсти лучше любых слов!",
                "flowers": [1],
                "color_scheme": "красный"
            },
            "5": {
                "pk": 5,
                "title": "Весеннее настроение",
                "price": 700,
                "budget_category": "~500",
                "image": "static/images/bouquet5.jpg",
                "occasion": "8 марта",
                "meaning": "Пробуждение природы в одном букете - свежесть и нежность весенних цветов!",
                "flowers": [2, 5, 7],
                "color_scheme": "разноцветный"
            },
            "6": {
                "pk": 6,
                "title": "Свежесть",
                "price": 900,
                "budget_category": "~1000",
                "image": "static/images/bouquet6.jpg",
                "occasion": "без повода",
                "meaning": "Свежий и яркий букет для поднятия настроения в любой день!",
                "flowers": [2, 4, 7],
                "color_scheme": "разноцветный"
            },
            "7": {
                "pk": 7,
                "title": "Изумруд",
                "price": 1500,
                "budget_category": "больше",
                "image": "static/images/bouquet7.jpg",
                "occasion": "свадьба",
                "meaning": "Роскошный букет для особенного торжества",
                "flowers": [1, 3, 6],
                "color_scheme": "красный"
            },
            "8": {
                "pk": 8,
                "title": "Вдохновение",
                "price": 550,
                "budget_category": "~500",
                "image": "static/images/bouquet8.jpg",
                "occasion": "1 сентября",
                "meaning": "Яркий букет для учителя к началу учебного года",
                "flowers": [4, 7],
                "color_scheme": "желтый"
            },
            "9": {
                "pk": 9,
                "title": "Гармония",
                "price": 1000,
                "budget_category": "~1000",
                "image": "static/images/bouquet9.jpg",
                "occasion": "день рождения",
                "meaning": "Сбалансированная композиция, которая подойдет всем",
                "flowers": [2, 3, 5],
                "color_scheme": "розовый"
            },
            "10": {
                "pk": 10,
                "title": "Эксклюзив",
                "price": 2200,
                "budget_category": "больше",
                "image": "static/images/bouquet10.jpg",
                "occasion": "свадьба",
                "meaning": "Уникальный букет для самого важного дня",
                "flowers": [1, 5, 6, 8],
                "color_scheme": "фиолетовый"
            },
            "11": {
                "pk": 11,
                "title": "Летняя свежесть",
                "price": 850,
                "budget_category": "~1000",
                "image": "static/images/bouquet11.jpg",
                "occasion": "без повода",
                "meaning": "Освежающий букет для жаркого летнего дня",
                "flowers": [2, 4, 7],
                "color_scheme": "разноцветный"
            },
            "12": {
                "pk": 12,
                "title": "Королевский прием",
                "price": 4800,
                "budget_category": "больше",
                "image": "static/images/bouquet12.jpg",
                "occasion": "день рождения",
                "meaning": "Роскошный букет для особого торжества",
                "flowers": [1, 3, 6, 8],
                "color_scheme": "фиолетовый"
            },
            "13": {
                "pk": 13,
                "title": "Весенний рассвет",
                "price": 650,
                "budget_category": "~500",
                "image": "static/images/bouquet13.jpg",
                "occasion": "8 марта",
                "meaning": "Нежные весенние цветы для самого нежного праздника",
                "flowers": [2, 5],
                "color_scheme": "розовый"
            },
            "14": {
                "pk": 14,
                "title": "Деловое настроение",
                "price": 1200,
                "budget_category": "~1000",
                "image": "static/images/bouquet14.jpg",
                "occasion": "1 сентября",
                "meaning": "Строгий и элегантный букет для деловой атмосферы",
                "flowers": [3, 8],
                "color_scheme": "синий"
            },
            "15": {
                "pk": 15,
                "title": "Огненная страсть",
                "price": 2800,
                "budget_category": "~2000",
                "image": "static/images/bouquet15.jpg",
                "occasion": "14 февраля",
                "meaning": "Пылающая страсть в каждом лепестке",
                "flowers": [1, 7],
                "color_scheme": "красный"
            },
            "16": {
                "pk": 16,
                "title": "Зимняя сказка",
                "price": 480,
                "budget_category": "больше",
                "image": "static/images/bouquet16.jpg",
                "occasion": "день рождения",
                "meaning": "Волшебство зимней сказки в изящной композиции",
                "flowers": [3, 6],
                "color_scheme": "белый"
            },
            "17": {
                "pk": 17,
                "title": "Осенняя гармония",
                "price": 950,
                "budget_category": "~1000",
                "image": "static/images/bouquet17.jpg",
                "occasion": "без повода",
                "meaning": "Теплые осенние краски для уютного настроения",
                "flowers": [4, 7, 8],
                "color_scheme": "желтый"
            },
            "18": {
                "pk": 18,
                "title": "Романтический вечер",
                "price": 800,
                "budget_category": "~2000",
                "image": "static/images/bouquet18.jpg",
                "occasion": "свадьба",
                "meaning": "Идеальное дополнение к романтическому вечеру",
                "flowers": [1, 2, 5],
                "color_scheme": "розовый"
            },
            "19": {
                "pk": 19,
                "title": "Солнечный привет",
                "price": 600,
                "budget_category": "~500",
                "image": "static/images/bouquet19.jpg",
                "occasion": "другой повод",
                "meaning": "Яркий букет, который подарит солнечное настроение",
                "flowers": [4, 7],
                "color_scheme": "фиолетовый"
            },
            "20": {
                "pk": 20,
                "title": "Элегантная простота",
                "price": 1900,
                "budget_category": "~2000",
                "image": "static/images/bouquet20.jpg",
                "occasion": "день рождения",
                "meaning": "Простота и элегантность в каждой детали",
                "flowers": [3, 8],
                "color_scheme": "белый"
            }
        },
        "color_schemes.json": {
            "1": {"pk": 1, "title": "красный"},
            "2": {"pk": 2, "title": "розовый"},
            "3": {"pk": 3, "title": "белый"},
            "4": {"pk": 4, "title": "желтый"},
            "5": {"pk": 5, "title": "фиолетовый"},
            "6": {"pk": 6, "title": "разноцветный"}
        },
        "occasions.json": {
            "1": {"pk": 1, "title": "день рождения"},
            "2": {"pk": 2, "title": "свадьба"},
            "3": {"pk": 3, "title": "1 сентября"},
            "4": {"pk": 4, "title": "8 марта"},
            "5": {"pk": 5, "title": "14 февраля"},
            "6": {"pk": 6, "title": "без повода"},
            "7": {"pk": 7, "title": "другой повод"}
        },
        "orders.json": {
            "1": {
                "pk": 1,
                "customer": 2,
                "bouquet": 1,
                "address": "пр. Ленина, д. 42",
                "delivery_date": "2024-07-15",
                "delivery_time": "14:00",
                "comment": "Позвонить за 15 минут до прибытия",
                "status": "доставлен",
            },
            "2": {
                "pk": 2,
                "customer": 1,
                "bouquet": 3,
                "address": "ул. Пушкина, д. 10, кв. 25",
                "delivery_date": "2024-07-16",
                "delivery_time": "18:30",
                "comment": "",
                "status": "в обработке",
            },
            "3": {
                "pk": 3,
                "customer": 2,
                "bouquet": 4,
                "address": "пр. Ленина, д. 42",
                "delivery_date": "2024-07-20",
                "delivery_time": "12:00",
                "comment": "Консультация с флористом: добавить больше зелени",
                "status": "консультация",
            }
        },
        "consultations.json": {
            "1": {
                "pk": 1,
                "customer": 2,
                "phone": "+79219876543",
                "occasion": "юбилей",
                "budget": 3000,
                "preferred_colors": ["красный", "белый"],
                "excluded_flowers": [3],
                "status": "обработан",
                "created_at": "2024-07-10T14:30:00",
            },
            "2": {
                "pk": 2,
                "customer": 1,
                "phone": "+79111234567", 
                "occasion": "свадьба",
                "budget": 5000,
                "preferred_colors": ["белый", "розовый"],
                "excluded_flowers": [],
                "status": "новый",
                "created_at": "2024-07-12T10:15:00",
            }
        },
        "roles.json": {
            "1": {"pk": 1, "title": "customer"},
            "2": {"pk": 2, "title": "manager"},
            "3": {"pk": 3, "title": "courier"}
        },
        "users.json": {
            "1": {
                "pk": 1,
                "tg_id": 123456789,
                "full_name": "Иван Иванов",
                "role": 1,
                "address": "ул. Пушкина, д. 10, кв. 25",
                "phone": "+79111234567"
            },
            "2": {
                "pk": 2,
                "tg_id": 987654321,
                "full_name": "Мария Петрова",
                "role": 1,
                "address": "пр. Ленина, д. 42",
                "phone": "+79219876543"
            },
            "3": {
                "pk": 3,
                "tg_id": 555555555,
                "full_name": "Анна Флористова",
                "role": 2,
                "address": "ул. Цветочная, д. 5",
                "phone": "+79105555555"
            },
            "4": {
                "pk": 4,
                "tg_id": 666666666,
                "full_name": "Петр Курьеров",
                "role": 3,
                "address": "ул. Доставки, д. 10",
                "phone": "+79106666666"
            }
        }
    }

    for filename, data in test_data.items():
        file_path = json_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Создан файл: {file_path}")

if __name__ == "__main__":
    create_test_json_files()