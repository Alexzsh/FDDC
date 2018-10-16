Min_prob = 1e-10


def viterbi(sentence, states, start_mat, trans_mat, obs_mat):
    # V=np.zeros([len(sentence),len(states)])
    V = [{}]
    path = {}
    for i, state in enumerate(states):
        V[0][state] = start_mat[state] * obs_mat[state].get(sentence[0], Min_prob)
        path[state] = [state]

    for i in range(1, len(sentence)):
        V.append({})
        new_path = {}
        for current_state in states:
            max_prob, state = max([(V[i - 1][pre_status] * trans_mat[pre_status].get(current_state, Min_prob) * obs_mat[current_state].get(sentence[i], Min_prob), pre_status) for pre_status in states])
            V[i][current_state] = max_prob
            new_path[current_state] = path[state] + [current_state]
        path = new_path
    (prob, state) = max([(V[len(sentence) - 1][y], y) for y in states])
    return (prob, path[state])
