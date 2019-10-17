#encoding=utf-8
import sys,os
#reload(sys)
#sys.setdefaultencoding('utf-8')
import random
import copy

class WordMerge:
    def __init__(self,params):
        self.words_path = params["words_path"]
        self.target_file = params["target_file"]
        self.target_single_file = params["target_single_file"]
        self.similar_rate = params["similar_rate"]
        self.words_dict = self.loadWords(self.words_path)
        self.distance_dict = {}
        self.similar_dict = {}
        pass

    def loadWords(self, words_path):
        words_dict = {}
        with open(words_path,'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().replace('\n','')
                line_list = line.split('\t')
                if len(line_list)!=2:
                    continue
                word = line_list[0]
                meaning = line_list[1]
                if word not in words_dict:
                    words_dict[word] = set()
                words_dict[word].add(meaning)
        return words_dict
         

    def strDistance(self,list1,list2):
        len_str1 = len(list1)+1
        len_str2 = len(list2)+1
        matrix = [[0]*(len_str2) for i in range(len_str1)]
        for i in range(len_str1):
            for j in range(len_str2):
                if i==0 and j==0:
                    matrix[i][j] = 0
                elif i==0 and j>0:
                    matrix[0][j] = j
                elif i>0 and j==0:
                    matrix[i][0] = i
                elif list1[i-1] == list2[j-1]:
                    matrix[i][j] = min(matrix[i-1][j-1],matrix[i][j-1]+1,matrix[i-1][j]+1)
                else:
                    matrix[i][j] = min(matrix[i-1][j-1]+1, matrix[i][j-1]+1,matrix[i-1][j]+1)
        return matrix[len_str1-1][len_str2-1]

    def getDistanceScore(self, word1, word2):
        key1 = word1+"_"+word2
        key2 = word2+"_"+word1
        if key1 in self.distance_dict:
            return self.distance_dict[key1]
        elif key2 in self.distance_dict:
            return self.distance_dict[key2]
        else:
            score = self.strDistance(word1, word2)
            self.distance_dict[key1] = score
            return score

    def isSimilar(self,word1, word2, score):
        length = max(len(word1),len(word2))
        #print(word1+' '+str(len(word1)) + ":"+word2+' '+str(len(word2)))
        if score<=(length-length/self.similar_rate):
            #print("    True : "+str(score)+" <= "+str(length-length/self.similar_rate)+" of "+str(length))
            #print('\n')
            return True
        else:
            #print("    False : "+str(score)+" <= "+str(length-length/self.similar_rate)+" of "+str(length))
            #print('\n')
            return False
        #return score<=(length-length/3)

    def mergeSimilar(self, temp_list, word="", recursive=True):
        #temp_words_dict = copy.deepcopy(words_dict)
        similar_list = list()
        final_list = list()
        if word=="":
            init_word = temp_list[random.randint(0,len(temp_list)-1)]
        else:
            init_word = word
        for word in temp_list:
            if word == init_word:
                continue
            score = self.getDistanceScore(word, init_word)
            if self.isSimilar(word, init_word, score):
               similar_list.append(word)
        if len(similar_list)==0:
            return False, [init_word]
        else:
            similar_list.append(init_word)
            if recursive:
                for word in similar_list:
                    _,result_list = self.mergeSimilar(temp_list, word=word, recursive=False)
                    final_list.extend(result_list)
                final_list.extend(similar_list)
                final_list = list(set(final_list))
                return True, final_list
            else:
                return True, similar_list

    def process(self):
        words_list = copy.deepcopy(list(self.words_dict.keys()))
        cluster_list = list()
        bad_list = list()
        while len(words_list)>0 :
            flag, result_list = self.mergeSimilar(words_list, recursive=False)
            if flag:
                cluster_list.append(result_list)
                new_list = list()
                for i in words_list:
                    if i not in result_list:
                        new_list.append(i)
                words_list = new_list
            else:
                bad_list.append(result_list[0])
                words_list.remove(result_list[0])
        self.writeResult(cluster_list, bad_list)
        return self.processSingleWord()

    def processSingleWord(self):
        single_dict = {}
        bad_list = list()
        for word in self.words_dict.keys():
            flag, result_list= self.mergeSimilar(self.words_dict, word=word, recursive=False)
            if flag:
                single_dict[word] = result_list
            else:
                bad_list.append(word)
        self.writeSingleResult(single_dict, bad_list)
        for word in bad_list:
            single_dict[word] = bad_list
        return single_dict, self.words_dict

    def writeSingleResult(self, single_dict, bad_list):
        with open(self.target_single_file,'w') as f:
            for k,v in single_dict.items():
                f.write(k+' : '+'\n')
                for i in v:
                    f.write("    "+i+'\n')
            f.write("bad : \n")
            for word in bad_list:
                f.write("    "+word+'\n')

    def writeResult(self, cluster_list, bad_list):
        with open(self.target_file,'w') as f:
            for cluster in cluster_list:
                for word in cluster:
                    f.write(word+'    '+','.join(self.words_dict[word])+'\n')
                f.write('\n')
            f.write("bad : \n")
            for word in bad_list:
                f.write("    "+word+'    '+','.join(self.words_dict[word])+'\n')

if __name__=='__main__':
    params = {}
    params["words_path"] = "./words2.txt"
    params["target_file"] = "./result.txt"
    params["target_single_file"] = "./single_result.txt"
    params["similar_rate"] = 2
    wordMerge = WordMerge(params)
    wordMerge.process()
    pass
