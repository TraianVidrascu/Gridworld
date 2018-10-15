from random import randint, sample

from gridworld.grid import Grid


class Policy:
    POLICY = [0.25, 0.25, 0.25, 0.25]

    def __init__(self):
        self.gamma = 0.9
        self.error = 0.0
        self.grid = Grid()
        self.state_values = [[]]
        self.state_policies = [[]]
        self.returns = [[]]

    def init(self):
        self.state_values = [[0.0 for e in range(5)] for e in range(5)]
        self.state_policies = [[Policy.POLICY for e in range(5)] for e in range(5)]
        self.error = 0.0001

    def episodic_eval_init(self):
        self.state_values = [[0.0 for e in range(5)] for e in range(5)]
        self.state_policies = [[Policy.POLICY for e in range(5)] for e in range(5)]
        self.returns = [[[] for e in range(5)] for e in range(5)]
        self.gamma = 1

    def iteration_init(self):
        self.state_values = [[0.0 for e in range(5)] for e in range(5)]
        self.state_policies = [[[1.0, 0.0, 0.0, 0.0] for e in range(5)] for e in range(5)]
        self.error = 0.0001

    def evaluate(self):
        while True:
            delta = 0
            for i in range(0, 5):
                for j in range(0, 5):
                    value = self.state_values[i][j]
                    self.state_values[i][j] = self.state_value_function(i, j)
                    delta = max(delta, abs(value - self.state_values[i][j]))
            if delta < self.error:
                break

    def state_value_function(self, x, y):
        actions_sum = 0
        for action in Grid.ACTIONS:
            action_policy = self.state_policies[x][y][action]
            reward, next_x, next_y = self.grid.move(x, y, action)
            actions_sum += action_policy * (reward + self.gamma * self.state_values[next_x][next_y])
        return actions_sum

    def maximum_action(self, x, y):
        value = -1000.0
        best = 0
        for action in Grid.ACTIONS:
            reward, next_x, next_y = self.grid.move(x, y, action)
            temp = reward + self.gamma * self.state_values[next_x][next_y]
            if temp > value:
                value = temp
                best = action
        return best

    def improve(self):
        policy_stable = True
        for i in range(0, 5):
            for j in range(0, 5):
                old_action = self.select_old_action(i, j)
                new_action = self.maximum_action(i, j)
                if new_action != old_action:
                    policy_stable = False
                    for k in range(0, 4):
                        if k == new_action:
                            self.state_policies[i][j][k] = 1
                        else:
                            self.state_policies[i][j][k] = 0
        return policy_stable

    def print_values(self):
        for i in range(0, len(self.state_values)):
            line = ""
            for j in range(0, len(self.state_values[i])):
                line += str(round(self.state_values[i][j], 1)) + " "
            print line

    def select_old_action(self, i, j):
        for k in range(0, 4):
            if self.state_policies[i][j][k] == 1:
                return k

    def evaluate_policy(self):
        self.init()
        self.evaluate()
        self.print_values()
        print "\n"

    def policy_iteration(self):
        self.iteration_init()
        while True:
            self.evaluate()
            stable = self.improve()
            if stable:
                break
        self.print_values()
        print "\n"

    def create_episode(self):
        episode = []

        while True:
            x = randint(0, 4)
            y = randint(0, 4)
            a, b, c = self.grid.is_special(x, y)
            if a == -1:
                break
        episode.append((0, x, y))

        while True:
            reward, next_x, next_y = self.grid.move_terminal(x, y, sample(Grid.ACTIONS, 1)[0])
            if x != -1 or y != -1:
                episode.append((reward + episode[-1][0], next_x, next_y,))
                x = next_x
                y = next_y
            else:
                break
        return episode

    def episodic_setup(self):
        self.episodic_eval_init()
        for i in range(200):
            episode = self.create_episode()
            for r, x, y in episode:
                g = float(episode[-1][0] - r)
                self.returns[x][y].append(g)
                self.state_values[x][y] = sum(self.returns[x][y]) / len(self.returns[x][y])
        self.print_values()
        print "\n"


p = Policy()
p.evaluate_policy()
p.policy_iteration()
p.episodic_setup()
