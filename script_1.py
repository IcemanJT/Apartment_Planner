import random
from deap import base, creator, tools
import matplotlib.pyplot as plt

# Definicja problemu - maksymalizacja dopasowania
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Parametry mieszkania
WIDTH = 20  # Szerokość mieszkania
HEIGHT = 15  # Wysokość mieszkania

# Parametry oczekiwane
NUM_SMALL = 15
NUM_LARGE = 3

# Funkcja generująca losowe pomieszczenie
def random_room():
    room_type = random.choice(["small", "large"])
    width = random.randint(1, 5) if room_type == "small" else random.randint(4, 10)
    height = random.randint(1, 5) if room_type == "small" else random.randint(4, 10)
    x = random.randint(0, WIDTH - width)
    y = random.randint(0, HEIGHT - height)
    return (x, y, width, height, room_type)

# Inicjalizacja populacji
def init_individual():
    num_rooms = NUM_SMALL + NUM_LARGE
    return creator.Individual([random_room() for _ in range(num_rooms)])

def init_population(n):
    return [init_individual() for _ in range(n)]

# Funkcja oceny
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

    small_count = sum(1 for room in ind if room[4] == "small")
    large_count = sum(1 for room in ind if room[4] == "large")

    size_penalty = abs(small_count - NUM_SMALL) + abs(large_count - NUM_LARGE)

    return -(overlap + holes * 4 + size_penalty),

# Operatory genetyczne
def mutate(ind):
    if random.random() < 0.5:
        index = random.randint(0, len(ind) - 1)  # Losowy indeks pomieszczenia
        room = list(ind[index])
        room[0] = random.randint(0, WIDTH - room[2])  # Nowe losowe x
        room[1] = random.randint(0, HEIGHT - room[3])  # Nowe losowe y
        ind[index] = tuple(room)  # Nadpisanie w rozwiązaniu
    else:
        index = random.randint(0, len(ind) - 1)
        ind[index] = random_room()  # Całkowicie nowe pomieszczenie
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
    pop = toolbox.population(n=50)
    NGEN = 1000
    CXPB, MUTPB = 0.5, 0.2

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
        plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor='black', facecolor=color, alpha=0.5))
    plt.xlim(0, WIDTH)
    plt.ylim(0, HEIGHT)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
