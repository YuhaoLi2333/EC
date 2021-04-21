'''
Author: your name
Date: 2020-11-16 23:17:47
LastEditTime: 2020-12-03 21:37:18
LastEditors: Please set LastEditors
Description: 本文件提供用于进化计算的通用父类
FilePath: /loan/EC/base_class.py
'''
import numpy as np
import copy
import random


class Individual():
    '''
    description: 个体类型
    '''
    def __init__(self, index, gene, is_descrete = None, bounds = None, param = None, fitness_func = None, **kwargs):
        '''
        description: 检查入参; 初始化个体
        param {
            ind: 产生的个体，ind类型列表
            geneNum: 基因个数
            index: 个体在群体中的编号
            isDescrete: 是否是离散型问题
            bounds: 每个变量的取值范围，为列表类型[gene_index: []]; 离散性问题为所有可能取值; 连续性问题只有2个元素，为变量的上下界: [下界, 上界];
            param: 用于评价个体的评价模型中的某些参数(字典类型)，如果没有则为None
            }
        '''
        # 校验入参类型
        isvalid = True
        msg = []
        if not (len(gene) == len(bounds)):
            raise ValueError('传入的gene个数、每个gene是否为离散变量列表个数和每个基因取值范围个数不相等')

        for gene_i in range(len(gene)):
            if not isinstance(gene[gene_i], int):
                msg.append(f'第{index}个个体的第{gene_i}个基因类型不为int')
                isvalid = False
            if not isinstance(is_descrete, int):
                msg.append(f'第{index}个个体的第{gene_i}个基因的离散/连续类型应该为bool值')
                isvalid = False
            if (not is_descrete) and (len(bounds[gene_i]) != 2):
                msg.append(f'第{index}个个体的第{gene_i}个(连续类型)基因的取值范围不正确')
                isvalid = False
            if not is_descrete and (bounds[gene_i][0] > bounds[gene_i][1]):
                msg.append(f'第{index}个个体的第{gene_i}个(连续类型)基因取值的下界大于上界')
                isvalid = False
            if len(bounds[gene_i]) == 0:
                msg.append(f'第{index}个个体的第{gene_i}个基因的取值范围为 None')
                isvalid = False

        if not isinstance(index, int):
            msg.append('个体在群体中的索引不为整数')
            isvalid = False

        if param != None:
            if not isinstance(param, dict):
                msg.append('传入的param参数不为字典类型')
                isvalid = False
        
        # if fitness_func != None:
        #     if not isinstance(fitness_func, callable):
        #         msg.append('传入的fitness_func参数不为callable类型')
        #         isvalid = False

        
        if not isvalid:
            print('!!!! ERROR !!!!')
            [print(item) for item in msg]
            raise TypeError(msg)
        
        # 校验基因类型
        self._index = index
        self._gene = np.array(gene)
        self._gene_num = len(gene)
        self._is_descrete = copy.deepcopy(is_descrete)
        self._bounds = copy.deepcopy(bounds)
        self._param = copy.deepcopy(param)
        self._fitness = None
        self.fitness_func = fitness_func
        if 'name' in kwargs.keys():
            self._name = kwargs['name']

    # def __repr__(self):
    #     try:
    #         return f'{self._name} fit: {self.fitness}'
    #     except:
    #         return f'{self.index} fit: {self.fitness}'
    
    def initilate(self):
        def get_random(a, b):
            '''
            返回1个[a,b)之间的随机数
            '''
            return (b - a) * np.random.random() + a
        # 如果是离散问题，则随机生成解
        if self.is_descrete:
            self.gene = [np.random.choice(self.bounds[g_i]) for g_i in range(self.gene_num)]
        # 如果是连续问题，则返回
        else:
            self.gene = [get_random(self.bounds[g_i][0], self.bounds[g_i][1]) for g_i in self.gene_num]
        pass
      
    # 设置 gene 字段
    @property
    def gene(self):
        return self._gene
    @gene.setter
    def gene(self, gene):
        self._gene = gene
    

    # 设置 fitness 字段
    @property
    def fitness(self):
        return self._fitness
    @fitness.setter
    def fitness(self, fitness):
        self._fitness = fitness

    
    # 设置 geneNum 字段
    @property
    def gene_num(self):
        return self._gene_num
    
    # 设置 index 字段
    @property
    def index(self):
        return self._index
    @index.setter
    def index(self, i):
        self._index = i

    # 设置 name 字段
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name
    
    # 设置 param 字段
    @property
    def param(self):
        return self._param
    @param.setter
    def param(self, param):
        self._param = param
    @param.deleter
    def param(self):
        del self._param

    # 设置 is_descrete 字段
    @property
    def is_descrete(self):
        return self._is_descrete

    # 设置 geneNum 字段
    @property
    def bounds(self):
        return self._bounds
    
    # # 设置 fitness_func 字段
    # @property
    # def fitness_func(self):
    #     return self._fitness_func
    # @fitness_func.setter
    # def fitness_func(self, fitness):
    #     self._fitness_func = fitness_func

class Population():
    '''
    description: 
    '''
    def __init__(self, pop, index):
        '''
        description: EC类提供基础类
        param {
            pop: 种群
            index: 种群索引
            }
        return {*}
        '''
        # 校验入参类型
        for i in range(len(pop)):
            if not isinstance(pop[i], Individual):
                raise TypeError(f'第{i}个个体类型不为Individual')
        if not isinstance(index, int):
            raise TypeError(f'第{i}个种群的索引不为整数')
        # 初始化种群
        self._pop = pop
        self._index = index
    
    # 设置 pop 字段
    @property
    def pop(self):
        return self._pop
    @pop.setter
    def pop(self, index, ind):
        self._pop[index] = ind
    
    @pop.deleter
    def pop(self, index, ind):
        del self._pop[index]
    
    # 设置 index 字段
    @property
    def index(self):
        return self._index

    def __repr__(self):
        return f'Pop: {self._index}'
    
class EC():
    def __init__(self, pop, pop_num = None, offsprint_num = None):
        '''
        description: EC类提供一些简单的通用操作子
        param {
            pop: 种群
            pop_num: 种群个数
            offsprintNum: 子代个数
            }
        '''
        # 校验入参类型
        for i in range(len(pop)):
            if not isinstance(pop[i], Individual):
                raise TypeError(f'第{i}个个体类型不为Individual')
        # 
        self._pop = pop
        self._pop_num = len(pop) if pop_num == None else pop_num
        self._offsprint_num = len(pop) if offsprint_num == None else offsprint_num
        self._children = []
        for i in range(offsprint_num):
            self._children.append(copy.deepcopy(self._pop[0]))
            self._children[i].initilate()
            self._children[i].index = i
            self._children[i].fitness = 0

    # 设置 pop 字段
    @property
    def pop(self):
        return self._pop
    
    @pop.setter
    def pop(self, index, ind):
        self._pop[index] = ind

    # 设置 pop_num 字段
    @property
    def pop_num(self):
        return self._pop_num
    
    @pop_num.setter
    def pop_num(self, index, ind):
        self._pop_num[index] = ind

    # 设置 children 字段
    @property
    def children(self):
        return self._children
    
    @children.setter
    def children(self, index, ind):
        self._children[index] = ind

    @children.deleter
    def children(self, index, ind):
        self._children[index] = ind

    # 设置 offsprintNum 字段
    @property
    def offsprint_num(self):
        return self._offsprint_num
    
    @offsprint_num.setter
    def offsprint_num(self, index, ind):
        self._offsprint_num[index] = ind

    '''
    提供一些通用的操作子
    '''
    # 随机生成k个不重复整数
    def _get_random_list(self, a:int, b: int, k: int):
        '''
        生成 k 个在 [a, b) 内 随机整数
        '''
        try:
            random_list = random.sample(range(a, b - 1), k)
            np.sort(random_list)
        except ValueError:
            raise ValueError(f'输入的k(={k})大于个体基因个数，生成变异基因位置失败')
        return random_list
    
    # 双个体: 多点交叉
    def crossover(self, parent1: Individual, parent2: Individual, child1: Individual, child2: Individual, k = 1):
        # # 生成k个不重复随机
        # try:
        #     random_list = random.sample(range(0, parent1.geneNum - 1), k)
        # except ValueError:
        #     raise ValueError(f'输入的k(={k})大于个体基因个数，生成交叉点失败')
        # # 父代个体基因交叉产生子代
        # random_list.sort()
        # is_crossover = False
        # child1.gene = parent1.gene
        # child2.gene = parent2.gene
        # for r_i in random_list:
        #     if is_crossover:
        #     else:
                
        pass
    

    # 多峰优化: 清楚
    def clearing(self):
        pass

    # 多峰优化: 拥挤度
    def crowding(self):
        pass

if __name__ == "__main__":
    tmppop = []
    for i in range(5):
        ind = Individual(i, [1,2,3,4], False, [[6,2,3]] * 4, name = f'{i}, {i}')
        tmppop.append(ind)
    pop = Population(tmppop, 0)