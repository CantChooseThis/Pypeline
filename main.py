import pygame as pg
from pype import Pype
from liquid import Liquid
import random
from resource import Resource
pg.init()
WIDTH, HEIGHT = 360, 576
WIN = pg.display.set_mode((WIDTH, HEIGHT))
NORTH, SOUTH, EAST, WEST = 0, 1, 2, 3
PROGRESS = pg.USEREVENT+1




def draw(all_pipes, liquids, tank, font=None):
    WIN.fill((0, 0, 0))
    for liquid in liquids:
        WIN.blit(liquid.surface, liquid.rect)
    for resource in tank:
        WIN.blit(resource.surface, resource.rect)
    for pipe in all_pipes:
        WIN.blit(pipe.surface, pipe.rect)
    if font != None:
        WIN.blit(font, font.get_rect(y=54, x=12))



    pg.display.update()


def check_filled(all_pipes):
    for pipe in all_pipes:
        # if pipe.filled or pipe.source:
        pipe.filledby = [
            pipe.connected(pipe.n[NORTH], NORTH) and pipe.n[NORTH].filled if pipe.n[NORTH] is not None else False,
            pipe.connected(pipe.n[SOUTH], SOUTH) and pipe.n[SOUTH].filled if pipe.n[SOUTH] is not None else False,
            pipe.connected(pipe.n[EAST], EAST) and pipe.n[EAST].filled if pipe.n[EAST] is not None else False,
            pipe.connected(pipe.n[WEST], WEST) and pipe.n[WEST].filled if pipe.n[WEST] is not None else False
        ]
        pipe.filled = pipe.filledby[0] or pipe.filledby[1] or pipe.filledby[2] or pipe.filledby[3] or pipe.source
        if pipe.filled:
            # create a variable to track if this function has filled an unfilled pipe
            end = False  # End of the line
            if pipe.n[NORTH] is not None:
                if not pipe.n[NORTH].filled:
                    end = pipe.connected(pipe.n[NORTH], NORTH)
                    pipe.n[NORTH].filled = pipe.connected(pipe.n[NORTH], NORTH)
                pipe.n[NORTH].filledby[SOUTH] = pipe.connected(pipe.n[NORTH], NORTH)
            if pipe.n[SOUTH] is not None:
                if not pipe.n[SOUTH].filled:
                    end = pipe.connected(pipe.n[SOUTH], SOUTH)
                    pipe.n[SOUTH].filled = pipe.connected(pipe.n[SOUTH], SOUTH)
                pipe.n[SOUTH].filledby[NORTH] = pipe.connected(pipe.n[SOUTH], SOUTH)
            if pipe.n[EAST] is not None:
                if not pipe.n[EAST].filled:
                    end = pipe.connected(pipe.n[EAST], EAST)
                    pipe.n[EAST].filled = pipe.connected(pipe.n[EAST], EAST)
                pipe.n[EAST].filledby[WEST] = pipe.connected(pipe.n[EAST], EAST)
            if pipe.n[WEST] is not None:
                if not pipe.n[WEST].filled:
                    end = pipe.connected(pipe.n[WEST], WEST)
                    pipe.n[WEST].filled = pipe.connected(pipe.n[WEST], WEST)
                pipe.n[WEST].filledby[EAST] = pipe.connected(pipe.n[WEST], WEST)
            if end:
                return 0

def gprint(grid):
    for row in grid:
        for col in row:
            print(' [', end='')
            for obj in col:
                print(str(obj), end="")
            # print(str(col), end="")
            print('] ', end='')
        print()


def flow(tank, objs):
    for resource in reversed(tank):
        if resource.stage == 0:  # if I'm in the top tank
            below = objs[resource.row()+1][resource.col()]  # Evaluate all objects below me
            # print(f"I am resource at row {resource.row()} and column {resource.col()}. I am checking one row below me.")
            canfall = True  # I'm going to check if I can fall
            for obj in below:  # Evaluate all objects below me
                if isinstance(obj, Resource):  # If the object is a resource
                    canfall = False  # I can't fall
                    # print(f"There is a resource at row {resource.row()+1} and column {resource.col()}")
                if isinstance(obj, Pype):  # If the object is a pipe
                    canfall = obj.open[0] and canfall  # I can fall if I could fall before & the pipe is open to me

            if canfall: # If I can fall
                # print("There should be no resources here.")
                type(objs[resource.row()][resource.col()].pop())  # Remove myself from my previous location
                resource.rect.y += 36  # Change my Y to move down
                myspot = objs[resource.row()][resource.col()]  # Check if I'm still in the top resevoir
                for obj in myspot:  # Evaluate all the objects in my new position
                    if isinstance(obj, Pype):  # If the object is a pipe
                        resource.stage = 1  # I'm now in the pypeline
                    if isinstance(obj, Resource):  # If there is a resource here, there is a problem
                        print(f"There is a resource in my spot! (Row: {resource.row()} | Col: {resource.col()})")
                objs[resource.row()][resource.col()].append(resource)  # Adds me to my new location
        elif resource.stage == 1:
            pipe = objs[resource.row()][resource.col()][0]  # I am in the pypeline, which means there is a pipe in my location.

            def down():
                below = objs[resource.row()+1][resource.col()]
                if len(below) == 0:
                    if pipe.open[SOUTH]:
                        resource.stage = 2
                        objs[resource.row()][resource.col()].pop()
                        resource.rect.y += 36
                        objs[resource.row()][resource.col()].append(resource)
                        return True
                elif isinstance(below[0], Pype) and pipe.connected(below[0], SOUTH):  # If the pipe below us is connected
                    canmove = True  # if there is no resource below me, then I can move down
                    for object in below:
                        if isinstance(object, Resource):
                            canmove = False
                    if canmove:
                        objs[resource.row()][resource.col()].pop()  # Remove myself from my previous location
                        resource.rect.y += 36  # Change my Y to move down
                        objs[resource.row()][resource.col()].append(resource)  # Add me to my new location in objs
                        return True
                return False

            def left():
                if resource.col() > 0:
                    left = objs[resource.row()][resource.col()-1]
                    if len(left) != 0 and isinstance(left[0], Pype) and pipe.connected(left[0], WEST):  # If the pipe left of us is connected
                        canmove = True  # If there is no resource left of me, then I can move left
                        for object in left:
                            if isinstance(object, Resource):
                                canmove = False
                        if canmove:
                            objs[resource.row()][resource.col()].pop()  # Remove myself from my previous location
                            resource.rect.x -= 36  # Change my X to move down
                            objs[resource.row()][resource.col()].append(resource)  # Add me to my new location in objs
                            return True
                return False

            def right():
                if resource.col() < 9:
                    right = objs[resource.row()][resource.col()+1]
                    if len(right) != 0 and isinstance(right[0], Pype) and pipe.connected(right[0], EAST):  # If the pipe left of us is connected
                        canmove = True  # If there is no resource left of me, then I can move right
                        for object in right:
                            if isinstance(object, Resource):
                                canmove = False
                        if canmove:
                            objs[resource.row()][resource.col()].pop()  # Remove myself from my previous location
                            resource.rect.x += 36  # Change my X to move down
                            objs[resource.row()][resource.col()].append(resource)  # Add me to my new location in objs
                            return True
                return False
            if not down():
                dir = [left, right]
                if not dir.pop(random.randint(0, 1))():
                    dir[0]()
        elif resource.stage == 2:
            if resource.row() < 15 and len(objs[resource.row()+1][resource.col()]) == 0:
                objs[resource.row()][resource.col()].pop()
                resource.rect.y += 36
                objs[resource.row()][resource.col()].append(resource)

    gprint(objs)


def main():
    objs = [[[] for y in range(WIDTH//36)] for x in range(HEIGHT//36)]
    tank = [Resource(x=i//3*36, y=i % 3 * 36) for i in range(30)] # y = 468
    for resource in tank:
        objs[resource.row()][resource.col()].append(resource)
    all_pipes = [Pype(x=i % 10*36, y=i//10*36+108) for i in range(100)]
    for pipe in all_pipes:
        objs[pipe.rect.y//36][pipe.rect.x//36].append(pipe)
    gprint(objs)
    for pipe in all_pipes:
        if pipe.rect.y > 108:
            pipe.n[NORTH] = [e for e in all_pipes if e.rect.x == pipe.rect.x and e.rect.y == pipe.rect.y-pipe.rect.height][0]
        if pipe.rect.y < 468-pipe.rect.height:
            pipe.n[SOUTH] = [e for e in all_pipes if e.rect.x == pipe.rect.x and e.rect.y == pipe.rect.y+pipe.rect.height][0]
        if pipe.rect.x < WIDTH-pipe.rect.width:
            pipe.n[EAST] = [e for e in all_pipes if e.rect.y == pipe.rect.y and e.rect.x == pipe.rect.x+pipe.rect.width][0]
        if pipe.rect.x > 0:
            pipe.n[WEST] = [e for e in all_pipes if e.rect.y == pipe.rect.y and e.rect.x == pipe.rect.x-pipe.rect.width][0]
    liquids = []
    all_pipes[0].source = True
    pg.time.set_timer(PROGRESS, 100)
    play = True
    counter = 0
    while play:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                play = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                left_click = pg.mouse.get_pressed(num_buttons=3)[0]
                clicked = [pipe for pipe in all_pipes if pipe.rect.collidepoint(pos)]
                for pipe in clicked:
                    pipe.rotate(-90 if left_click else 90)
                    counter += 1
                    print(pipe.open)
            if event.type == PROGRESS:
                # check_filled(all_pipes)
                # liquids = [pipe.liquid for pipe in all_pipes if pipe.filled]
                flow(tank, objs)
                won = True
                for resource in tank:
                    if resource.row() < 13:
                        won = False
                if won:
                    message = f"You won in {pg.time.get_ticks() // 1000} seconds, and in {counter} moves"
                    cali = pg.font.Font("CALIBRI.TTF", 20).render(message, True, (255, 255, 255))
                    draw(all_pipes, liquids, tank, font=cali)
                    while True:
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                play = False
        pg.display.set_caption(f"Pypeline - {counter} moves")

        draw(all_pipes, liquids, tank)


if __name__ == "__main__":
    main()
