import random
from flask import Flask, session, request, render_template, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Розміри лабіринту
N = 5


# Генерація лабіринту
def generate_maze():
    maze = [[0 for _ in range(N)] for _ in range(N)]
    path = []
    print(maze)


    def path_finder(x, y):
        maze[x][y] = 1
        path.append((x, y))
        if (x, y) == (N - 1, N - 1):
            return True
        directions = ['D', 'R', 'U', 'L']
        random.shuffle(directions)
        for direction in directions:
            if direction == 'D':
                new_x, new_y = x + 1, y
            elif direction == 'R':
                new_x, new_y = x, y + 1
            elif direction == 'U':
                new_x, new_y = x - 1, y
            elif direction == 'L':
                new_x, new_y = x, y - 1
            if 0 <= new_x < N and 0 <= new_y < N and maze[new_x][new_y] == 0:
                if path_finder(new_x, new_y):
                    return True

        return False

    path_finder(0, 0)


    return maze


# Перевірка, чи можна перейти до клітинки
def move_is_safe(maze, x, y):
    return 0 <= x < N and 0 <= y < N and maze[x][y] == 1


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'maze' not in session or 'position' not in session:
        # Генеруємо новий лабіринт та встановлюємо початкову позицію
        maze = generate_maze()
        session['maze'] = maze
        session['position'] = [0, 0]
    else:
        maze = session['maze']
        position = session['position']

    message = ""
    if request.method == 'POST':
        move = request.form.get('move')
        x, y = session['position']

        if move == 'L':
            new_x, new_y = x, y - 1
            direction = "вліво"
        elif move == 'R':
            new_x, new_y = x, y + 1
            direction = "вправо"
        elif move == 'U':
            new_x, new_y = x - 1, y
            direction = "вгору"
        elif move == 'D':
            new_x, new_y = x + 1, y
            direction = "вниз"
        else:
            message = "Невірний вибір! Виберіть 'Вліво', 'Вправо', 'Вгору' або 'Вниз'."
            return render_template('index.html', maze=maze, position=session['position'], message=message, N=N)

        if move_is_safe(maze, new_x, new_y):
            session['position'] = [new_x, new_y]
            position = session['position']
            message = f"Ви просунулись на клітинку {direction}."
        else:
            message = f"Неможливо перейти {direction}, там стіна!"

    position = session['position']
    if position == [N - 1, N - 1]:
        message = "Вітаємо! Ви знайшли вихід з лабіринту!"
    return render_template('index.html', maze=maze, position=position, message=message, N=N, enumerate=enumerate)


@app.route('/reset')
def reset():
    # Очищення сесії для створення нового лабіринту
    session.pop('maze', None)
    session.pop('position', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)


