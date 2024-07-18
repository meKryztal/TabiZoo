# Автофарм TabiZoo
![photo_2024-07-18_21-45-38](https://github.com/user-attachments/assets/3909d25e-22ab-40b5-87fe-d81b7b889d26)


-  Клеймит каждые 8 часов поинты
-  Забирает дейли ревард
-  Можно загрузить сотни акков
-  Работа по ключу, без авторизации
-  Сам улучшает акк



# Установка:
1. Установить python (Протестировано на 3.11)

2. Зайти в cmd(терминал) и вписывать
   ```
   git clone https://github.com/meKryztal/TabiZoo.git
   ```
   ```
   cd TabiZoo
   ```
3. Установить модули
   
   ```
   pip install -r requirements.txt
   ```
 
   или
   
   ```
   pip3 install -r requirements.txt
   ```



4. Запуск
   ```
   python tabi.py
   ```

   или

   ```
   python3 tabi.py
   ```
   

   
Вставить в файл init_data ключи такого вида, каждый новый ключ с новой строки:
   ```
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   ```
Вместо query_id= может быть user=, разницы нету
# Как получить query_id:
Заходите в telegram web, открываете бота, жмете F12 или в десктопной версии открывайте окно, правой кнопкой жмете и выбираете самое нижнее "проверить" и переходите в Network, жмете старт в веб версии или перезагружаете страницу в десктопной, ищете запрос с именем info, в правой колонке находите Rawdata: query_id=бла бла бла или user=
![photo_2024-07-18_21-54-55](https://github.com/user-attachments/assets/7e432a6f-d944-406b-80fd-0a3931b1876e)



