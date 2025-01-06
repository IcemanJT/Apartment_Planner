import random
from deap import base, creator, tools
import matplotlib.pyplot as plt


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

WIDTH = 20
HEIGHT = 15

NUM_SMALL = 12
NUM_LARGE = 5


def random_room(room_type):
    width = random.randint(1, 5) if room_type == "small" else random.randint(5, 10)
    height = random.randint(1, 5) if room_type == "small" else random.randint(5, 10)
    x = random.randint(0, WIDTH - width)
    y = random.randint(0, HEIGHT - height)
    return (x, y, width, height, room_type)


def init_individual():
    rooms = ["large"] * NUM_LARGE + ["small"] * NUM_SMALL
    return creator.Individual([random_room(type) for type in rooms])


def init_population(n):
    return [init_individual() for _ in range(n)]


def evaluate(ind):
    covered_area = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    overlap = 0
    for room in ind:
        x, y, w, h, _ = room
        for i in range(x, x + w):
            for j in range(y, y + h):
                if 0 <= i < WIDTH and 0 <= j < HEIGHT:
                    if covered_area[j][i] == 1:
                        overlap += 1
                    covered_area[j][i] = 1

    total_area = sum(sum(row) for row in covered_area)
    holes = WIDTH * HEIGHT - total_area

    return -(overlap * 2 + holes),


def mutate(ind):
    index = random.randint(0, len(ind) - 1)
    type = ind[index][4]
    ind[index] = random_room(type)
    return ind,


toolbox = base.Toolbox()
toolbox.register("individual", init_individual)
toolbox.register("population", init_population)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selTournament, tournsize=3)


# Główna pętla ewolucyjna
def main():
    pop = toolbox.population(n=200)
    NGEN = 2000
    CXPB, MUTPB = 0.75, 0.35

    for gen in range(NGEN):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]
        print(f"Generation {gen}: Max fitness = {max(fits)}")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual:", best_ind)

    draw_solution(best_ind)

# Wizualizacja rozwiązania
def draw_solution(ind):
    plt.figure(figsize=(10, 7))
    for room in ind:
        x, y, w, h, room_type = room
        color = 'blue' if room_type == "small" else 'red'
        plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor='black', facecolor=color, alpha=0.5, linewidth=2))
    plt.xlim(0, WIDTH)
    plt.ylim(0, HEIGHT)
    plt.show()

if __name__ == "__main__":
    main()
