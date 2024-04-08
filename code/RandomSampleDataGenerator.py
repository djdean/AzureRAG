import random, string
from essential_generators import DocumentGenerator
class RandomSampleDataGenerator():
    def __init__(self, num_samples, schema, llm_handler, random_word_length, random_int_range):
        self.num_samples = num_samples
        self.schema = schema
        self.llm_handler = llm_handler
        self.random_word_length = random_word_length
        self.random_int_range = random_int_range
    def generate_single_sample(self, schema, generator):
        sample = {}
        data = generator.sentence()
        data_vector = self.llm_handler.generate_embeddings(data)  
        letters = string.ascii_lowercase
        for key in schema:
            element_data = schema[key]
            if isinstance(element_data, str):
                str_data = schema[key]
                str_split = str_data.split("|")
                if len(str_split) > 1:
                    gentype = str_split[1]
                    if gentype == "NAME":
                        sample[key] = generator.name()
                    elif gentype == "EMAIL":
                        sample[key] = generator.email()
                    elif gentype == "PHONE":
                        sample[key] = generator.phone()
                    elif gentype == "WORD":
                        if len(str_split[0]) > 0:
                            sample[key] = str_split[0]+"_"+generator.word()
                        else:
                            sample[key] = generator.word()
                    else:
                        base_content = str_split[0]+"_"
                        random_content = ''.join(random.choice(letters) for i in range(self.random_word_length))
                        sample[key] = base_content + random_content
                else:
                    sample[key] = str_data
            elif isinstance(element_data, list):
                sample[key] = data_vector
            elif isinstance(element_data,int):
                sample[key] = random.randint(0,self.random_int_range)
        sample["content"] = data
        sample["contentVector"] = data_vector
        return sample
    def generate_samples(self):
        samples = []
        generator = DocumentGenerator()
        for i in range(self.num_samples):
            sample = self.generate_single_sample(self.schema, generator)
            samples.append(sample)
        return samples