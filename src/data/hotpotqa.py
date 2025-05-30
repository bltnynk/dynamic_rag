from typing import Dict, List
import logging
import os
import json
from tqdm import tqdm
from datasets import Dataset
from .base_dataset import BaseDataset

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

class HotpotQA(BaseDataset):
    examplars: List[Dict] = [
        {
            'question': "Jeremy Theobald and Christopher Nolan share what profession?",
            'cot': "Jeremy Theobald is an actor and producer. Christopher Nolan is a director, producer, and screenwriter. Therefore, they both share the profession of being a producer.",
            'answer': "producer",
        },
        {
            'question': "What film directed by Brian Patrick Butler was inspired by a film directed by F.W. Murnau?",
            'cot': "Brian Patrick Butler directed the film The Phantom Hour. The Phantom Hour was inspired by the films such as Nosferatu and The Cabinet of Dr. Caligari. Of these Nosferatu was directed by F.W. Murnau.",
            'answer': "The Phantom Hour.",
        },
        {
            'question': "How many episodes were in the South Korean television series in which Ryu Hye-young played Bo-ra?",
            'cot': "The South Korean television series in which Ryu Hye-young played Bo-ra is Reply 1988. The number of episodes Reply 1988 has is 20.",
            'answer': "20",
        },
        {
            'question': "Were Lonny and Allure both founded in the 1990s?",
            'cot': "Lonny (magazine) was founded in 2009. Allure (magazine) was founded in 1991. Thus, of the two, only Allure was founded in 1990s.", 
            'answer': "no",
        },
        {
            'question': "Vertical Limit stars which actor who also played astronaut Alan Shepard in \"The Right Stuff\"?",
            'cot': "The actor who played astronaut Alan Shepard in \"The Right Stuff\" is Scott Glenn. The movie Vertical Limit also starred Scott Glenn.",
            'answer': "Scott Glenn",
        },
        {
            'question': "What was the 2014 population of the city where Lake Wales Medical Center is located?",
            'cot': "Lake Wales Medical Center is located in the city of Polk County, Florida. The population of Polk County in 2014 was 15,140.",
            'answer': "15,140",
        },
        {
            'question': "Who was born first? Jan de Bont or Raoul Walsh?",
            'cot': "Jan de Bont was born on 22 October 1943. Raoul Walsh was born on March 11, 1887. Thus, Raoul Walsh was born the first.",
            'answer': "Raoul Walsh",
        },
        {
            'question': "In what country was Lost Gravity manufactured?",
            'cot': "The Lost Gravity (roller coaster) was manufactured by Mack Rides. Mack Rides is a German company.",
            'answer': "Germany",
        },
        {
            'question': "Which of the following had a debut album entitled \"We Have an Emergency\": Hot Hot Heat or The Operation M.D.?",
            'cot': "The debut album of the band \"Hot Hot Heat\" was \"Make Up the Breakdown\". The debut album of the band \"The Operation M.D.\" was \"We Have an Emergency\".",
            'answer': "The Operation M.D.",
        },
        {
            'question': "How many awards did the \"A Girl Like Me\" singer win at the American Music Awards of 2012?",
            'cot': "The singer of \"A Girl Like Me\" singer is Rihanna. In the American Music Awards of 2012, Rihana won one award.",
            'answer': "one",
        },
        {
            'question': "The actor that stars as Joe Proctor on the series \"Power\" also played a character on \"Entourage\" that has what last name?",
            'cot': "The actor that stars as Joe Proctor on the series \"Power\" is Jerry Ferrara. Jerry Ferrara also played a character on Entourage named Turtle Assante. Thus, Turtle Assante's last name is Assante.",
            'answer': "Assante",
        },
    ]

    demo_input_template = lambda self, ques: f'Question: {ques}\nAnswer:'
    test_input_template = lambda self, ques: f'Answer the following question by reasoning step-by-step, following the example above.\nQuestion: {ques}\nAnswer:' 
    output_template = lambda self, cot, ans: f'{cot} So the answer is {ans}.'

    def __init__(self, data_path: str):
        logger.info(f"Loading HotpotQA from {data_path}")
        dataset = []
        with open(os.path.join(data_path, 'hotpotqa-dev.json'), "r") as fin:
            js = json.load(fin)
            for example in tqdm(js):
                qid = example["_id"]
                question = example["question"]
                answer = example['answer']
                context = example['context']
                dataset.append({
                    'qid': qid,
                    'question': question,
                    'answer': answer,
                    # 'ctxs': context,
                })
        self.dataset = Dataset.from_list(dataset)
