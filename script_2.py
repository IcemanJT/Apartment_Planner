import random
import matplotlib.pyplot as plt
from deap import base, creator, tools

# Define DEAP creator for fitness and individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def calculate_area(room):
    (x1, y1), (x2, y2) = room["coordinates"]
    return abs(x2 - x1) * abs(y2 - y1)

def calculate_overlap(room1, room2):
    (x1, y1), (x2, y2) = room1["coordinates"]
    (x3, y3), (x4, y4) = room2["coordinates"]
    overlap_width = max(0, min(x2, x4) - max(x1, x3))
    overlap_height = max(0, min(y2, y4) - max(y1, y3))
    return overlap_width * overlap_height

def calculate_overlap_penalty(individual):
    penalty = 0
    for i, room1 in enumerate(individual):
        for j, room2 in enumerate(individual):
            if i != j:
                penalty += calculate_overlap(room1, room2)
    return penalty

def fitness_function(individual, width, height, num_small, num_large):
    total_area = width * height
    room_areas = sum(calculate_area(room) for room in individual)
    overlap_penalty = calculate_overlap_penalty(individual)
    return abs(total_area - room_areas) * 2 + overlap_penalty * 3,

def generate_room(area, room_type, width, height):
    if room_type == "small":
        target_area = area   # Small rooms occupy smaller area
    else:
        target_area = area * 2

    x1 = random.randint(0, width - 1)
    y1 = random.randint(0, height - 1)
    w = random.randint(1, width // 3 if room_type == "small" else width)
    h = target_area // w
    x2 = min(x1 + w, width)
    y2 = min(y1 + h, height)
    return {"type": room_type, "coordinates": ((x1, y1), (x2, y2))}

def generate_individual(width, height, num_small, num_large):
    total_area = width * height
    individual = []

    for _ in range(num_small):
        individual.append(generate_room(total_area / (num_small + num_large), "small", width, height))

    for _ in range(num_large):
        individual.append(generate_room(total_area / (num_small + num_large), "large", width, height))

    return creator.Individual(individual)

def mutate_individual(individual, width, height, num_small, num_large):
    total_area = width * height
    idx = random.randint(0, len(individual) - 1)
    room_type = individual[idx]["type"]
    individual[idx] = generate_room(total_area / (num_small + num_large), room_type, width, height)

def visualize_solution(solution, width, height):
    fig, ax = plt.subplots()
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)

    for room in solution:
        (x1, y1), (x2, y2) = room["coordinates"]
        color = 'lightgreen' if room["type"] == "small" else 'lightblue'
        rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor='black', facecolor=color, alpha=0.7)
        ax.add_patch(rect)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def main():
    width, height = 20, 20
    num_small, num_large = 10, 10
    generations, pop_size = 3000, 50

    toolbox = base.Toolbox()
    toolbox.register("individual", generate_individual, width, height, num_small, num_large)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness_function, width=width, height=height, num_small=num_small, num_large=num_large)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_individual, width=width, height=height, num_small=num_small, num_large=num_large)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=pop_size)

    for gen in range(generations):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.7:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < 0.2:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring

        fits = [ind.fitness.values[0] for ind in population]
        print(f"Generation {gen}: Max fitness = {min(fits)}")

    best_ind = tools.selBest(population, 1)[0]
    visualize_solution(best_ind, width, height)

if __name__ == "__main__":
    main()
