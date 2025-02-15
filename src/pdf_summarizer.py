import asyncio
from ollama_api_client import OllamaAPIClient
from utils import split_text_into_slices
import queue

class PDFSummarizer:
    def __init__(self, api_key, model, prompt_template_page, prompt_template_final):
        self.result_queue = queue.Queue()
        self.api_client = OllamaAPIClient(api_key)
        self.model = model,
        self.prompt_template_page = prompt_template_page
        self.prompt_template_final = prompt_template_final

    def summarize_slice(self, text_slices):
        summaries = []
        for slice in text_slices:
            prompt = self.summarize_prompt(slice)
            summary = asyncio.run(self.api_client.summarize_text(prompt))
            if summary == "cancelled" or self.api_client.is_cancelled():
                return summaries
            summaries.append(summary)
        return summaries

    def summarize_collected_summaries(self, summaries):
        """Summarize the collected summaries using the API client"""
        final_summary = asyncio.run(self.api_client.summarize_text(self.finalize_prompt(summaries)))
        return final_summary

    def write_summaries(self, filename, summaries):
        """Write the collected summaries to a file"""
        with open(f"{filename}_slice_summary.md", "w", encoding="utf-8") as f:
            if len(summaries) == 1:
                f.write(summaries[0])
            else:
                for summary in summaries:
                    f.write(summary + "\n\n")

    def pdf_summary(self, filename, extracted_text, write_to_local):
        text_slices = split_text_into_slices(extracted_text)
        
        summaries = self.summarize_slice(text_slices)
        if write_to_local:
            self.write_summaries(filename, summaries)

        final_summary = self.summarize_collected_summaries(summaries)
        if write_to_local:
            self.write_summaries(filename, [final_summary])
            print("Final Summary written to:", filename, "_summary.md")

        self.result_queue.put({
            "slice_summaries": summaries,
            "final_summary": final_summary
        })

    def summarize_prompt(self, text):
        prompt_template = """
        {prompt_template}
        {text}
        """
        prompt = prompt_template.format(prompt_template=self.prompt_template_page, text=text)
        return prompt

    def finalize_prompt(self, summaries):
        combined_summary = "\n\n".join(summaries)
        prompt_template = """
        {prompt_template}
        {text}
        """
        prompt = prompt_template.format(prompt_template=self.prompt_template_final, text=combined_summary)
        return prompt