import os
import gradio as gr
from app.controllers.retrieval.RetrieverEngine import RetrieverEngine

class AgiUIInterface:
    def __init__(self):
        # Initialize the AgikbQueryEngine
        self.agikb_engine = RetrieverEngine()
    
    def query_response(self, message, history):
        payload = {'query': message}
        # Query the AgikbQueryEngine
        system_msg, results = self.agikb_engine.query(
            payload['query']
        )
        print('====system_msg=====',system_msg)
        # Extract the appropriate response from 'results'
        response = results if results else "I'm not sure how to respond to that."
        if 'groupedResult' in results[0]['_additional']['generate']:
            grouped_result = results[0]['_additional']['generate']['groupedResult']
            print(grouped_result)
            print("=================================",grouped_result,'=================================')
        else:
            print("groupedResult not found")
        return grouped_result

    def launch_interface(self):
        # Create and launch the Gradio chat interface
        gr_interface = gr.ChatInterface(fn=self.query_response)
        gr_interface.launch()

# Create an instance of the class and launch the interface
# agikb_interface = AgikbQueryInterface()
# agikb_interface.launch_interface()
