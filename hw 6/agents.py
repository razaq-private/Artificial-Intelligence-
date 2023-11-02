# Include your imports here, if any are used.

student_name = "Type your full name here."

# 1. Value Iteration


class ValueIterationAgent:

    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.game = game
        self.discount = discount
        self.values = {}
        # TODO

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        vals = self.values.get(state, 0)
        return vals  # TODO

    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        T = self.game.get_transitions(state, action)
        Q = 0
        for next_state, probability in T.items():
            reward = self.game.get_reward(state, action, next_state)
            Q += probability * (reward + (self.discount
                                          * self.get_value(next_state)))
        return Q  # TODO

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        if state in self.game.states:
            actions = self.game.get_actions(state)
            best_action = None
            best_Q = -float('inf')

            for action in actions:
                Q = self.get_q_value(state, action)
                if Q > best_Q:
                    best_Q = Q
                    best_action = action
            return best_action
        return None  # TODO

    def iterate(self):
        """Run single value iteration using Bellman equation:
        V_{k+1}(s) = max_a Q*(s,a)
        Then update values: V*(s) = V_{k+1}(s)
        """
        new_vals = {}
        states = self.game.states
        for state in states:
            new_vals[state] = max(self.get_q_value(state, action)
                                  for action in self.game.get_actions(state))

        self.values = new_vals
        # TODO

# 2. Policy Iteration


class PolicyIterationAgent(ValueIterationAgent):

    """Implement Policy Iteration Agent.

    The only difference between policy
    iteration and value iteration is at
    their iteration method. However, if
    you need to implement helper function or
    override ValueIterationAgent's methods,
    you can add them as well.
    """
    def iterate(self):
        """Run single policy iteration.
        Fix current policy, iterate state values
        V(s) until |V_{k+1}(s) - V_k(s)| < ε
        """
        epsilon = 1e-6

        while True:
            diff = 0

            for state in self.game.states:
                value = self.get_value(state)
                new_value = self.get_q_value(state,
                                             self.get_best_policy(state))
                diff = abs(new_value - value)
                self.values[state] = new_value

            if diff < epsilon:
                break
            # TODO

# 3. Bridge Crossing Analysis


def question_3():
    discount = 0.9
    noise = 0.0
    return discount, noise


# 4. Policies


def question_4a():
    discount = 0.2
    noise = 0.0
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4b():
    discount = 0.2
    noise = 0.1
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4c():
    discount = 0.9
    noise = 0.0
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4d():
    discount = 0.9
    noise = 0.2
    living_reward = 0.5
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4e():
    discount = 0.9
    noise = 0.9
    living_reward = 0.9
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


# 5. Feedback
# Just an approximation is fine.
feedback_question_1 = 4

feedback_question_2 = """
The conversion from policy iteration
to value iteration
"""

feedback_question_3 = """
Liked the guess and check
portion
"""
