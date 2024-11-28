import agentboard as ab
from agentboard.utils import function_to_schema

def run_agent_order_coffee():
    """
        agentboard --logdir=./log
        # agentboard --logdir=./log --logfile=xxx.log --static=./static --port=5000
    """
    with ab.summary.FileWriter(logdir="./log", static="./static") as writer:

        agent_name = "agent_ordering_coffee"
        ab.summary.agent_loop(name="START", data="This is start stage of %s", agent_name = agent_name, process_id="START", workflow_type="start", duration = 0)

        ## Planning Stage
        ab.summary.agent_loop(name="PLAN INPUT", data={"task": "Plan Input"}, agent_name = agent_name, process_id="PLAN", duration = 0)
        ab.summary.agent_loop(name="PLAN EXECUTION", data={"task": "This is Plan EXECUTION"}, agent_name = agent_name, process_id="PLAN", duration = 0)
        ab.summary.agent_loop(name="PLAN OUTPUT", data={"task": "Plan Output"}, agent_name = agent_name, process_id="PLAN", duration = 0)

        ## required parameters 
        user_prompt = "Hi, I would like to order a cup of Starbucks coffee"
        ab.summary.agent_loop(name="PROMPT", data={"prompt": user_prompt}, agent_name = agent_name, process_id="QUERY UNDERSTANDING", duration = 0)

        ## QU Code of NLP Models
        ## Code Ingored

      
        qu_result = {"cup_size": None, "brand": "Starbucks"}
        ab.summary.agent_loop(name="QU OUTPUT", data=qu_result, agent_name = agent_name, process_id="QUERY UNDERSTANDING", duration = 0)

        ## QU Code of NLP Models, Calling LLM wiht tools [request_other_parameters(), order_coffee()]
        def request_other_parameters():
            return
        def order_coffee():
            return

        tools = [request_other_parameters, order_coffee]
        ab.summary.agent_loop(name="LLM Function INPUT", data={"tools": [function_to_schema(tool) for tool in tools] }, agent_name=agent_name, process_id="LLM Function Calls 1", duration = 0)
        ab.summary.agent_loop(name="LLM Function OUTPUT", data={"tools": [function_to_schema(request_other_parameters)] }, agent_name=agent_name, process_id="LLM Function Calls 1", duration = 0)

        ## DECISON
        ab.summary.agent_loop(name="IF Make New Request", data={"tools": [ function_to_schema(request_other_parameters) ]}, agent_name = agent_name, process_id="NEW REQUEST", workflow_type="decision",duration = 0)

        ## Make New Request
        tool_name = "request_other_parameters"
        tool_params = {"args": "cup_size"}
        response_text = "What cup size of coffee do you want?"

        ab.summary.agent_loop(name="OPTION 1", data={"name": tool_name, "params": tool_params}, agent_name = agent_name, process_id="OPTIONS", duration = 0)
        ab.summary.agent_loop(name="OPTION 2", data={}, agent_name = agent_name, process_id="OPTIONS", duration = 0)

        user_input = "Grande"
        ab.summary.agent_loop(name="USER INPUT", data=user_input, agent_name=agent_name, process_id="USER", duration = 0)

        ### Calling LLM Tool user
        params = {"cup_size": user_input, "brand": "Starbucks"}
        ab.summary.agent_loop(name="LLM Function INPUT", data=params, agent_name=agent_name, process_id="LLM Function Calls 2", duration = 0)
        ab.summary.agent_loop(name="LLM Function OUTPUT", data={"name": order_coffee.__name__, "params": params}, agent_name = agent_name, process_id="LLM Function Calls 2", duration = 0)

        ### Execution
        ab.summary.agent_loop(name="ORDER EXECUTION", data=params, agent_name=agent_name, process_id="Order Execution", duration = 0)

        ### Response Generation
        prompt = "Please Generate a Response to User and Tell the user status of the order"
        order_status = "success"
        params = {"status": order_status}
        ab.summary.agent_loop(name="LLM GENERATION OUTPUT", data={"prompt": prompt, "params": params}, agent_name = agent_name, process_id="LLM Generation Response", duration = 0)

        ### Final Response
        final_response = "Your order for grande cup size Starbucks coffee is successfull and the order ID is: 123456"
        ab.summary.agent_loop(name="ORDER STATUS", data={"status": order_status, "reply": final_response}, agent_name = agent_name, process_id="REPLY", duration = 0)

        ## END
        ab.summary.agent_loop(name="END", data="This is End Stage of Agent Ordering Coffee Loop", agent_name = agent_name, process_id="END", workflow_type="start", duration = 0)

if __name__ == "__main__":
    run_agent_order_coffee()
