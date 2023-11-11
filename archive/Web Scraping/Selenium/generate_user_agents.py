from latest_user_agents import get_latest_user_agents, get_random_user_agent

def generate_random_user_agents():
    lst = get_latest_user_agents()
    user_agents_list = ['user-agent']*len(lst)

    user_agents = []
    for user_agent_string, user_agent in zip(user_agents_list, lst):
        user_agent = f"\"'{user_agent_string}':'{user_agent}'\""
        print(user_agent)
        user_agents.append(user_agent)

    return user_agents

generate_random_user_agents()