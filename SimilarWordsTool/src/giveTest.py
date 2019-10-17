#encoding=utf-8
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from merge import *
import copy
import random

class GiveTest:
    def __init__(self,params):
        self.question_num = params["question_num"]
        self.selection_num = params["selection_num"]
        self.wordMerge = WordMerge(params)
        self.single_dict, self.words_dict = self.wordMerge.process()
        self.used_words = list()
        pass

    def giveOneTest(self, word, words_dict, single_dict):
        pass

    def selectWords(self, word, words_dict, single_dict, num):
        self.used_words.append(word)
        word_similar_list = self.cleanList(single_dict.get(word,list()))
        if len(word_similar_list)==num:
            word_similar_list.append(word)
            return word_similar_list
        elif len(word_similar_list)>num:
            random.shuffle(word_similar_list)
            result_list = word_similar_list[:num]
            result_list.append(word)
            self.used_words.extend(result_list)
            return result_list
        else:
            self.used_words.extend(word_similar_list)
            temp_words_dict = self.cleanList(list(words_dict.keys()))
            random.shuffle(temp_words_dict)
            result_list = temp_words_dict[:num-len(word_similar_list)]
            self.used_words.extend(result_list)
            word_similar_list.extend(result_list)
            word_similar_list.append(word)
            return word_similar_list
        pass

    def oneTest(self, word, num):
        select_words_list = self.selectWords(word, self.words_dict, self.single_dict, num)
        answer_str = self.combineTest(select_words_list)
        return answer_str

    def combineTest(self, select_words_list):
        length = len(select_words_list)
        answer_list = list(range(0,length))
        random.shuffle(answer_list)
        answer_str = ""
        for i in answer_list:
            answer_str+=str(i+1)
        selections_list = list(range(0,length))
        for num in range(len(answer_list)):
            index = answer_list[num]
            selections_list[index] = ','.join(self.words_dict[select_words_list[num]])
        for word in select_words_list:
            print(word)
        print("-------------------------------")
        selection_str = ""
        for num in range(len(selections_list)):
            selection_str += "(%d)%s    "%(num+1,selections_list[num])
        print(selection_str)
        #print("==============over=============")
        return answer_str

    def cleanList(self,input_list):
        new_list = list()
        for word in input_list:
            if word not in self.used_words:
                new_list.append(word)
        return new_list

    def process(self):
        question_count = 0
        correct_count = 0
        for num in range(0,self.question_num):
            clean_words_list = self.cleanList(self.words_dict.keys())
            if len(clean_words_list)==0:
                break
            index = random.randint(0,len(clean_words_list)-1)
            print("========(%d) quesition=========="%(num+1))
            answer_str = self.oneTest(clean_words_list[index],self.selection_num-1)
            answer = input("the sort answer is : ")
            if str(answer) == "exit":
                break
            if str(answer) == "pass":
                print("OK SKIP")
                continue
            if str(answer)==str(answer_str):
                print("Correct!")
                question_count += 1
                correct_count += 1
            else:
                question_count += 1
                print("Wrong ! the answer is %s"%(answer_str))
        print("accuary is %f"%(float(correct_count/question_count)))
             


if __name__=='__main__':
    params = {}
    params["words_path"] = "./words3.txt"
    params["target_file"] = "./result.txt"
    params["target_single_file"] = "./single_result.txt"
    params["similar_rate"] = 2
    params["question_num"] = 1000
    params["selection_num"] = 4
    giveTest = GiveTest(params)
    giveTest.process()
    pass
