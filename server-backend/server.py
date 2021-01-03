import asyncio
import websockets
import threading
from game import ServerGame, Empty
from database import db_store, db_add
from room import make_room, ServerRoom
from log_in import login
from perf_calc import get_data

rooms = dict()

async def interact(sock, path):
    global games
    global idn_curr
    idn = idn_curr
    idn_curr += 1

    print(f'Connected {idn}')
    
    player = None
    game = Empty()

    while True:
        command = await sock.recv()
        head,cont = command.split('|')

        print(idn,head,cont)
        new_id = '-'

        if head == 'BYE':
            sock.close()
            break

        if head == 'START':
            w,h,m = map(int,cont.split())
            game = ServerGame(w,h,m,player)

        if head == 'MOVE':
            x,y = map(int,cont.split())
            l = game.click(x,y)    
            
        if head == 'FLAG':
            x,y = map(int,cont.split())
            l = game.flag(x,y)    

        if head == 'RENAME':
            playerC, pwdC = cont.split()

            player = login(playerC,pwdC)
            print(player)
            
            if game != None:
                game.player = player

        if head == 'CREATE ROOM':
            w,h,m = map(int, cont.split())
            
            room_id, room = make_room(w,h,m)
            rooms[room_id] = room

            new_id = f'{room_id}'

        if head == 'JOIN ROOM':
            if player == None:
                await sock.send('PLAYER MUST HAVE ID TO JOIN ROOM')
                continue

            room_id = cont
            if room_id not in rooms:
                await sock.send('ROOM ID DOES NOT EXIST')
                continue

            game = rooms[room_id].join_room(player)
            x,y = game.height//2,game.width//2
            l = game.reveal(x,y)

        if head == 'DATABASE':
            user = cont.strip()
            ret_string = get_data(user)
            print(ret_string)
            
            await sock.send(ret_string)
            continue
            
        game_string = game.rep()
        await sock.send(new_id + ' ' + game_string)
       
                
idn_curr = 0

db_manager = threading.Thread(target=db_store)
db_manager.start()

start_server = websockets.serve(interact, "", 1321)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
