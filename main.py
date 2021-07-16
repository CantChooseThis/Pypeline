import pygame as pg
from pype import Pype
from liquid import Liquid
from resource import Resource
pg.init()
WIDTH, HEIGHT = 360, 576
WIN = pg.display.set_mode((WIDTH, HEIGHT))
NORTH, SOUTH, EAST, WEST = 0, 1, 2, 3
PROGRESS = pg.USEREVENT+1


def draw(all_pipes, liquids, tank):
    WIN.fill((0, 0, 0))
    for liquid in liquids:
        WIN.blit(liquid.surface, liquid.rect)
    for pipe in all_pipes:
        WIN.blit(pipe.surface, pipe.rect)
    for resource in tank:
        WIN.blit(resource.surface, resource.rect)

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
       if resource.stage == 0:
           below = objs[resource.col()][resource.row()-1]
           resource_below = False
           for obj in below:
            if isinstance(obj, Resource):
                resource_below = True
            if not resource_below:
                objs[resource.col()][resource.row()].pop()
                resource.rect.y += 36
                objs[resource.col()][resource.row()].append(resource)


def main():
    objs = [[[] for y in range(WIDTH//36)] for x in range(HEIGHT//36)]
    tank = [Resource(x=i//3*36, y=i % 3 * 36) for i in range(30)]
    for resource in tank:
        objs[resource.rect.y//36][resource.rect.x//36].append(resource)
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
    pg.time.set_timer(PROGRESS, 5000)
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
                    print(pipe.filledby)
            if event.type == PROGRESS:
                check_filled(all_pipes)
                liquids = [pipe.liquid for pipe in all_pipes if pipe.filled]
        pg.display.set_caption(f"Pypeline - {counter} moves")

        draw(all_pipes, liquids, tank)


if __name__ == "__main__":
    main()
