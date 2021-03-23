import asyncio, websockets
from collections import deque

# Modifiable parameters
user = "BOT[example_name]"
pwd = "example_pwd"
size_x = 30
size_y = 24
mines = 180
disp_game = False
disp_results = True
games = 1

flag_queue = deque()
click_queue = deque()

import random
async def bot(board, size_x, size_y, m):
    global click_queue, flag_queue
    
    # Example Bot
    unknown = []
    for x in range(size_x):
        for y in range(size_y):
            if board[y][x] == '-1':
                unknown.append((x,y))
    move = random.choice(unknown)

    click_queue.append(move)

async def play():
    global user, pwd, size_x, size_y, mines
    global disp_game, disp_results, click_queue, flag_queue, games
    server = ""
    async with websockets.connect(server) as server:
        await server.send(f'RENAME|{user} {pwd}')
        data = await server.recv()
        while games:
            games -= 1
            await server.send(f'CREATE_ROOM|{size_x} {size_y} {mines}')
            data = await server.recv()
            room_id = data.split()[1]
            await server.send(f'JOIN_ROOM|{room_id}')
            data = await server.recv()
            _, _, x, y, m, sc, stat, lb_len, *rest = data.split()
            x, y, m = map(int,(x, y, m))
            while stat == "1":
                c = 4*int(lb_len)
                lb = rest[:c]
                board = []
                for i in range(y):
                    board.append(rest[c+i*x:c+(i+1)*x])
                if disp_game:
                    print()
                    for i in board:
                        print(' '.join(i))
                    print()
                await bot(board, x, y, m)
                while click_queue:
                    x, y = click_queue.popleft()
                    await server.send(f'MOVE|{y} {x}')
                    data = await server.recv()
                while flag_queue:
                    x, y = flag_queue.popleft()
                    await server.send(f'FLAG|{y} {x}')
                    data = await server.recv()
                _, _, x, y, m, sc, stat, lb_len, *rest = data.split()
                x, y, m = map(int,(x, y, m))
            if disp_results:
                print(f'Score: {sc}/{x*y-m}')

asyncio.get_event_loop().run_until_complete(play())
