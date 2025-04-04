from .base_rag import BasicRAG

class SingleRAG(BasicRAG):
    def __init__(self, args):
        super().__init__(args)
    
    def inference(self, questions, demos, cases, view_uncertainty=True):
        assert self.query_formulation == "direct"
        docs = [self.retrieve(question, topk=self.retrieve_topk) for question in questions]
        # 对 topk 个 passage 生成 prompt
        prompt = "".join([d["case"]+"\n" for d in demo])
        prompt += "Context:\n"
        for i, doc in enumerate(docs):
            prompt += f"[{i+1}] {doc}\n"
        prompt += "Answer in the same format as before.\n"
        prompt += case
        prompts = []
        for demo, case in zip(demos, cases):
            prompt = "".join([d["case"]+"\n" for d in demo])
            prompt += "Context:\n"
            for i, doc in enumerate(docs):
                prompt += f"[{i+1}] {doc}\n"
            prompt += "Answer in the same format as before.\n"
            prompt += case
            prompts.append(prompt)
        return_dict = self.generator.generate(prompts, self.generate_max_length)
        text = return_dict['text']
        inference_results = dict(text=text)
        if view_uncertainty:
            token_uncertainty = list(zip(return_dict['tokens'], return_dict['entropies'], return_dict['logprobs']))
            inference_results['token_uncertainty'] = token_uncertainty
        return inference_results
