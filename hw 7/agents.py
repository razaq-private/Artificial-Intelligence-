import random

student_name = "Abudurazaq Aribidesi"


# 1. Q-Learning
class QLearningAgent:
    """Implement Q Reinforcement Learning Agent using Q-table."""

    def __init__(self, game, discount, learning_rate, explore_prob):
        """Store any needed parameters into the agent object.
        Initialize Q-table.
        """
        # TODO
        self.game = game
        self.discount = discount
        self.learning_rate = learning_rate
        self.explore_prob = explore_prob
        self.q_table = {}

    def get_q_value(self, state, action):
        """Retrieve Q-value from Q-table.
        For an never seen (s,a) pair, the Q-value is by default 0.
        """
        return self.q_table.get((state, action), 0)  # TODO

    def get_value(self, state):
        """Compute state value from Q-values using Bellman Equation.
        V(s) = max_a Q(s,a)
        """
        # if list of q vals is not empty return max of list else return 0
        actions = self.game.get_actions(state)
        if not actions:
            return 0

        vals = max([self.get_q_value(state, action) for action in actions])
        return vals  # TODO

    def get_best_policy(self, state):
        """Compute the best action to
        take in the state using Policy Extraction.
        π(s) = argmax_a Q(s,a)

        If there are ties, return a random one for better performance.
        Hint: use random.choice().
        """
        actions = self.game.get_actions(state)
        if not actions:
            return None
        max_q = self.get_value(state)
        best_policy = []
        for action in actions:
            if self.get_q_value(state, action) == max_q:
                best_policy.append(action)
        return random.choice(best_policy)  # TODO

    def update(self, state, action, next_state, reward):
        """Update Q-values using running average.
        Q(s,a) = (1 - α) Q(s,a) + α (R + γ V(s'))
        Where α is the learning rate, and γ is the discount.

        Note: You should not call this function in your code.
        """
        Q = self.get_q_value(state, action)
        V = self.get_value(next_state)
        updated_Q = ((1 - self.learning_rate) * Q +
                     self.learning_rate * (reward + self.discount * V))
        self.q_table[(state, action)] = updated_Q  # TODO

    # 2. Epsilon Greedy
    def get_action(self, state):
        """Compute the action to take for the agent, incorporating exploration.
        That is, with probability ε, act randomly.
        Otherwise, act according to the best policy.

        Hint: use random.random() < ε to check if exploration is needed.
        """
        actions = self.game.get_actions(state)
        if random.random() < self.explore_prob:
            actions = list(self.game.get_actions(state))
            return random.choice(actions)
        else:
            return self.get_best_policy(state)  # TODO


# 3. Bridge Crossing Revisited
def question3():
    epsilon = ...
    learning_rate = ...
    # return epsilon, learning_rate
    return 'NOT POSSIBLE'


# 5. Approximate Q-Learning
class ApproximateQAgent(QLearningAgent):
    """Implement Approximate Q Learning Agent using weights."""

    def __init__(self, *args, extractor):
        """Initialize parameters and store the feature extractor.
        Initialize weights table."""

        super().__init__(*args)
        self.extractor = extractor
        self.w_table = {}
        # TODO

    def get_weight(self, feature):
        """Get weight of a feature.
        Never seen feature should have a weight of 0.
        """
        return self.w_table.get(feature, 0)  # TODO

    def get_q_value(self, state, action):
        """Compute Q value based on the dot
        product of feature components and weights.
        Q(s,a) = w_1 * f_1(s,a) + w_2 * f_2(s,a) + ... + w_n * f_n(s,a)
        """
        extract = self.extractor(state, action)
        Q = 0
        for feature, value in extract.items():
            weight = self.get_weight(feature)
            Q += weight * value
        return Q  # TODO

    def update(self, state, action, next_state, reward):
        """Update weights using least-squares approximation.
        Δ = R + γ V(s') - Q(s,a)
        Then update weights: w_i = w_i + α * Δ * f_i(s, a)
        """
        # TODO
        V = self.get_value(next_state)
        Q = self.get_q_value(state, action)
        delta = reward + self.discount * V - Q
        extract = self.extractor(state, action)

        for feature, value in extract.items():
            new_weight = (self.w_table.get(feature, 0) +
                          self.learning_rate * delta * value)
            self.w_table[feature] = new_weight


# 6. Feedback
# Just an approximation is fine.
feedback_question_1 = 3

feedback_question_2 = """
the get action took
a while to understand
"""

feedback_question_3 = """
Liked the pacman poriton
"""
