# Инициализация карты
def init_map(width, height, custom=False):
    if custom:
        width = int(input("Введите ширину карты: "))
        height = int(input("Введите высоту карты: "))
    # Создаём карту: '#' - стена, '.' - пустое место
    game_map = [['#' if i == 0 or i == height - 1 or j == 0 or j == width - 1 else '.'
                 for j in range(width)] for i in range(height)]
    return game_map, width, height


# Рендер карты
def render_map(game_map, player, enemy):
    # Без очистки консоли, просто выводим карту
    for i, row in enumerate(game_map):
        for j, cell in enumerate(row):
            if (i, j) == (player['y'], player['x']):
                print('P', end=' ')  # Игрок
            elif (i, j) == (enemy['y'], enemy['x']):
                print('E', end=' ')  # Враг
            else:
                print(cell, end=' ')
        print()
    # Отображение характеристик
    print(f"\nPlayer: HP={player['hp']}, MP={player['mp']}, ARM={player['arm']}, DMG={player['dmg']}")
    print(f"Enemy: HP={enemy['hp']}, MP={enemy['mp']}, ARM={enemy['arm']}, DMG={enemy['dmg']}")
    # Debug-консоль
    print(f"Debug: Player at ({player['x']}, {player['y']}), Enemy at ({enemy['x']}, {enemy['y']})")


# Проверка коллизии
def check_collision(x, y, game_map, width, height, other_entity):
    if (x < 0 or x >= width or y < 0 or y >= height or
            game_map[y][x] == '#' or (x, y) == (other_entity['x'], other_entity['y'])):
        return True
    return False


# Перемещение игрока
def move_player(player, direction, game_map, width, height, enemy):
    new_x, new_y = player['x'], player['y']
    if direction == 'w':
        new_y -= 1
    elif direction == 's':
        new_y += 1
    elif direction == 'a':
        new_x -= 1
    elif direction == 'd':
        new_x += 1
    if not check_collision(new_x, new_y, game_map, width, height, enemy):
        player['x'], player['y'] = new_x, new_y
    return player


# Перемещение врага (без random, циклический выбор направления)
def move_enemy(enemy, game_map, width, height, player, move_counter):
    directions = ['w', 's', 'a', 'd']
    direction = directions[move_counter % 4]  # Циклически выбираем направление
    new_x, new_y = enemy['x'], enemy['y']
    if direction == 'w':
        new_y -= 1
    elif direction == 's':
        new_y += 1
    elif direction == 'a':
        new_x -= 1
    elif direction == 'd':
        new_x += 1
    if not check_collision(new_x, new_y, game_map, width, height, player):
        enemy['x'], enemy['y'] = new_x, new_y
    return enemy


# Расчёт урона
def calculate_damage(attacker, defender):
    damage = max(0, attacker['dmg'] - defender['arm'])  # Простая формула
    defender['hp'] = max(0, defender['hp'] - damage)
    print(f"Debug: {attacker['name']} deals {damage} damage to {defender['name']}")
    return defender


# Основная функция игры
def main():
    # Инициализация персонажей
    player = {'name': 'Player', 'x': 1, 'y': 1, 'hp': 100, 'mp': 50, 'arm': 10, 'dmg': 20}
    enemy = {'name': 'Enemy', 'x': 5, 'y': 5, 'hp': 80, 'mp': 30, 'arm': 5, 'dmg': 15}

    # Выбор типа карты
    map_type = input("Выберите тип карты (1 - стандартная, 2 - пользовательская): ")
    game_map, width, height = init_map(10, 10, map_type == '2')

    # Счётчик ходов для врага
    move_counter = 0

    # Основной игровой цикл
    while player['hp'] > 0 and enemy['hp'] > 0:
        render_map(game_map, player, enemy)
        action = input("\nВыберите действие (w/a/s/d - двигаться, k - атаковать, q - выйти): ").lower()

        if action in ['w', 'a', 's', 'd']:
            player = move_player(player, action, game_map, width, height, enemy)
            enemy = move_enemy(enemy, game_map, width, height, player, move_counter)
            move_counter += 1
        elif action == 'k':
            if abs(player['x'] - enemy['x']) + abs(player['y'] - enemy['y']) == 1:  # Рядом
                enemy = calculate_damage(player, enemy)
                if enemy['hp'] > 0:
                    player = calculate_damage(enemy, player)
        elif action == 'q':
            break

    # Итог игры
    render_map(game_map, player, enemy)
    if player['hp'] <= 0:
         print("Игрок проиграл!")
    elif enemy['hp'] <= 0:
        print("Игрок победил!")

# Запуск игры
main()