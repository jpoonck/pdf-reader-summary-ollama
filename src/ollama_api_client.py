from ollama import AsyncClient, ChatResponse
import threading
import asyncio

class OllamaAPIClient:
    def __init__(self, model, api_key):
        self.api_key = api_key
        self.model = model
        self.cancel_flag = threading.Event()
    
    def cancel(self):
        self.cancel_flag.set()

    def is_cancelled(self):
        return self.cancel_flag.is_set()

    async def check_cancel(self, flag):
        while True:
            if flag.is_set():
                raise asyncio.CancelledError("Summarization was cancelled.")
            await asyncio.sleep(1)

    async def summarize_text(self, text):
        if self.cancel_flag.is_set():
            return "cancelled"
        
        # Start the stream and create a task to monitor cancellation
        response_task = asyncio.create_task(AsyncClient().chat(model=self.model, messages=[{
            'role': 'user',
            'content': text,
        }]))

        # Create a task to check for cancellation while waiting
        cancel_monitor_task = asyncio.create_task(self.check_cancel(self.cancel_flag))
        
        try:
            print("waiting summarizing")
            # Wait for the stream response and cancellation monitor
            done, pending = await asyncio.wait(
                [response_task, cancel_monitor_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            if response_task in done:
                response = await response_task
                return response.message.content
            else:
                response_task.cancel()
                raise asyncio.CancelledError("Summarization was cancelled.")
        except asyncio.CancelledError:
            return "cancelled"

    async def summarize_summaries(self, summaries):
        combined_summary = "\n\n".join(summaries)
        return await self.summarize_text(combined_summary)