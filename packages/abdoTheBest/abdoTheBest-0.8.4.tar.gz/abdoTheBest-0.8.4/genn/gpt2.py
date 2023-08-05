
import torch
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel, AdamW, WarmupLinearSchedule
from numpy.random import choice
from genn.controllers import checkParams, readFiles, timeChecker, getStartWords, checkFileParams, checkProb, selectNucleus, chooseFromTop
import time


class GPT2:
	@checkParams(dict, str, int,(int, type(None)), (str, type(None)), (int, type(None)), (str, type(None)), (dict, type(None)), (dict, type(None)), (dict, type(None)))
	def __init__(self, fileParams, taskToken,
						epochs,
						instanceMxLen = None,
						variant="small",
						batchSize=32,
						eos="<|endoftext|>",
						seedParams={'N_first': 1, 'minFreq': 5},
						optimParams={"lr": 3e-4},
						schedParams={"warmup_steps": 400}):

		self.device = torch.device(
			'cuda' if torch.cuda.is_available() else 'cpu')
  
		self.__eos = eos
		self.__taskToken = taskToken
		self.__instanceMxLen = instanceMxLen
		self.__optimParams = optimParams
		self.__schedParams = schedParams

		self.__epochs = epochs
		self.__batchSize = batchSize
		self.__seedParams = seedParams
		self.__variant = self.__checkVariant(variant)
		self.__fileName, self.__fileExtension, self.__parsingColumn = checkFileParams(
			fileParams)

		self.__examples = None
		self.__seeds = None
		self.__model = None
		
		self.__getModel()
		self.__tokenizer = self.__getTokenizer()
		self.__optimizer = self.__getOptimizer()
		self.__scheduler = self.__getScheduler()
		self.__readFile()

	def __checkVariant(self, variant):
		avl = ["small", "medium", "large"]
		variant = variant.lower()
		if variant not in avl:
			raise Warning("Available variants are", " ".join(avl),
							"got", variant, "instead")

		# in PyTorch implementation, small = gpt2, medium = gpt2-medium etc.
		elif variant != 'small':
			return f'gpt2-{variant}'
		return 'gpt2'
	
	def __readFile(self):
		text = readFiles(self.__fileName, self.__fileExtension, self.__parsingColumn)

		if self.__instanceMxLen == None:
			self.__instanceMxLen = len(max(text, key=len))
		self.__examples = [f"{self.__taskToken} : {inst} {self.__eos}" for inst in text 
							if len(inst)>0]

		self.__seeds = getStartWords(self.__seedParams, text)

	def getSeed(self):
		"""
			return a weighted seed. 
			In case static seed is enabled, then the most frequent token will be the seed.
		"""
		seeds = list(self.__seeds.keys())
		probs = list(self.__seeds.values())
		return choice(seeds, 1 , probs).tolist()

	def __getBatches(self):            
		numBatches = len(self.__examples) // self.__batchSize
		for i in range(0, numBatches*self.__batchSize, self.__batchSize):
			yield self.__examples[i:i+self.__batchSize]

	def __encodeBatch(self, batch):
		encoded = torch.Tensor().long().to(self.device)
		for inst in batch:
			docTens = torch.tensor(self.__tokenizer.encode(inst)).unsqueeze(0).to(self.device)
			encoded = torch.cat([encoded, docTens[:,1:]], dim=1)
		return encoded


	def __getOptimizer(self):
		return AdamW(self.__model.parameters(), **self.__optimParams)

	def __getModel(self):
		self.__model = GPT2LMHeadModel.from_pretrained(self.__variant)
		self.__model = self.__model.to(self.device)
		self.__model.train()

	def __getTokenizer(self):
		return GPT2Tokenizer.from_pretrained(self.__variant)

	def __getScheduler(self):
		return WarmupLinearSchedule(self.__optimizer, t_total = -1, **self.__schedParams)
	
	def run(self):
		sumLoss = 0.0
		batchCount = 0
		lastLoss = None
		batchesLen = (len(self.__examples) // self.__batchSize) * self.__epochs

		for e in range(self.__epochs):
			batches = self.__getBatches()
			batchTimes = []
			for batch in batches:
				startTime = time.time()

				encoded = self.__encodeBatch(batch)

				outputs = self.__model(encoded, labels=encoded)

				loss, _ = outputs[:2]                        
				loss.backward()
				sumLoss += loss.detach().data

				batchCount += 1
				self.__optimizer.step()
				self.__scheduler.step() 
				self.__optimizer.zero_grad()
				self.__model.zero_grad()

				batchTime = time.time() - startTime
				batchTimes.append(batchTime)

				timeChecker(batchTimes, batchCount, batchesLen, e, self.__epochs, lastLoss)
				
			lastLoss = sumLoss
			sumLoss = 0.0

	@checkParams(int, (str, type(None)), (int, type(None)), (int, type(None)), (float, type(None)), (bool, type(None)))
	def generateDocument(self, n, selection='nucleus', genIter=None, k=5, prob=0.8, uniq=True):
		selection = selection.lower() 
		maxLen = genIter if genIter else self.__instanceMxLen
		prob = checkProb(prob)

		self.__model.eval()
		res = set()
		with torch.no_grad():
			while len(res) < n:
				curIds = torch.tensor(self.__tokenizer.encode(f"{self.__taskToken} {self.getSeed()[0]}")).unsqueeze(0).to(self.device)

				for _ in range(maxLen):
					outputs = self.__model(curIds, labels=curIds)
					_, logits = outputs[:2]

					if selection in 'nucleus':
						nextTokenId = selectNucleus(logits[0,-1], p=prob)

					else: #topk
						nextTokenId = chooseFromTop(logits[0,-1], n=k)

					curIds = torch.cat([curIds.long() ,torch.tensor([[nextTokenId]]).long()], dim = 1)
					if nextTokenId in self.__tokenizer.encode(self.__eos):
						break

				doc = self.__tokenizer.decode(list(curIds.squeeze().to('cpu').numpy())[2:]).strip()
				if uniq:
					if doc not in self.__examples:
						res.add(doc)
				else:
					res.add(doc)

		return list(res)


