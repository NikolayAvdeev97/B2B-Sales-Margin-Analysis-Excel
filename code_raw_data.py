import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_capstone_data():
    print("Генерация финального экзаменационного датасета (250 000 строк)...")
    
    # 1. Справочник товаров
    products = pd.DataFrame({
        'ProductID': [f'PRD-{i}' for i in range(1, 11)],
        'ProductName': [
            'Ноутбук Pro 15', 'Ноутбук Basic 13', 'Смартфон X', 'Смартфон Y', 
            'Планшет Z', 'Наушники Pro', 'Наушники Basic', 'Чехол кожаный', 
            'Защитное стекло', 'Кабель Type-C'
        ],
        'Category': [
            'Ноутбуки', 'Ноутбуки', 'Смартфоны', 'Смартфоны', 
            'Планшеты', 'Аудио', 'Аудио', 'Аксессуары', 
            'Аксессуары', 'Аксессуары'
        ],
        'BasePrice': [120000, 60000, 80000, 40000, 30000, 15000, 5000, 3000, 1000, 800],
        'CostPrice': [90000, 45000, 60000, 30000, 22000, 9000, 2000, 500, 100, 100]
    })
    products.to_excel('catalog.xlsx', index=False)
    
    # 2. Справочник промокодов (УСЛОЖНЕНИЕ: Разные типы скидок)
    promos = pd.DataFrame({
        'PromoCode': ['NO_PROMO', 'WINTER10', 'NEWYEAR20', 'GIFT5000'],
        'DiscountType': ['None', 'Percent', 'Percent', 'Flat'],
        'DiscountValue': [0, 10, 20, 5000] # Flat означает минус 5000 рублей от чека
    })
    promos.to_csv('promo_rules.csv', sep=';', index=False)
    
    # 3. Транзакции (Декабрь 2025)
    num_rows = 250000
    start_date = datetime(2025, 12, 1)
    
    dates = [start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23)) for _ in range(num_rows)]
    
    # Распределение вероятностей для промокодов
    promo_choices = np.random.choice(
        ['NO_PROMO', 'WINTER10', 'NEWYEAR20', 'GIFT5000'], 
        num_rows, 
        p=[0.4, 0.3, 0.2, 0.1]
    )
    
    # Распределение товаров (дешевые покупают чаще)
    product_choices = np.random.choice(
        products['ProductID'], 
        num_rows, 
        p=[0.05, 0.05, 0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.1, 0.1]
    )
    
    df = pd.DataFrame({
        'OrderID': [f'ORD-{100000 + i}' for i in range(num_rows)],
        'Date': dates,
        'ProductID': product_choices,
        'PromoCode': promo_choices,
        'Qty': np.random.randint(1, 4, num_rows)
    })
    
    # Внедрение небольшого мусора для этапа очистки
    df.loc[np.random.choice(df.index, 100), 'Qty'] = -1
    
    # Внедрение бизнес-аномалии (Маркетологи раздали купон на 5000 руб, но забыли поставить ограничение на минимальную сумму заказа. Его применяют на чехлы и кабели)
    bug_mask = (df['PromoCode'] == 'GIFT5000') & (df['ProductID'].isin(['PRD-8', 'PRD-9', 'PRD-10']))
    # Искусственно увеличиваем количество таких заказов во второй половине декабря, когда купон завирусился в интернете
    late_dec_mask = df['Date'] > datetime(2025, 12, 15)
    combined_mask = bug_mask & late_dec_mask
    df.loc[combined_mask, 'Qty'] = np.random.randint(5, 15, combined_mask.sum())
    
    df.to_csv('december_sales.csv', sep=';', index=False)
    print("Готово! Созданы файлы: december_sales.csv, catalog.xlsx, promo_rules.csv")

if __name__ == "__main__":
    generate_capstone_data()