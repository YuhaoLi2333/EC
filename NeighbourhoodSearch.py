'''
Author: your name
Date: 2020-11-27 22:43:41
LastEditTime: 2020-12-03 21:36:15
LastEditors: Please set LastEditors
Description: 本文件提供 领域搜索(neighbourhood search) 类
FilePath: /tianchi/EC/NeighbourhoodSearch.py
'''
import numpy as np
import random
import copy
import json
import os

from .base_class import Individual, Population, EC

class NeighbourhoodSearch(EC):
    def __init__(self, pop, pop_num = None, offsprint_num = None):
        super(NeighbourhoodSearch, self).__init__(pop = pop, pop_num = pop_num, offsprint_num = offsprint_num)
        for i in range(self.offsprint_num):
            del self.children[i].param
        self.history = {}

    # 单个体: 多基因变异
    def _mutation_operation(self, parent: Individual, children: list, k = 1, is_synchronous = False):
        # 执行变异操作
        def mutation(parent: Individual, child: Individual):
            # 随机选择k个基因
            gene_index_list = self._get_random_list(a = 0, b = parent.gene_num, k = k)
            gene_value_list = []
            # 遍历每个变异基因
            for g_i in gene_index_list:
                # 不允许变异成相同基因
                is_valid = False
                while not is_valid:
                    value = np.random.choice(parent.bounds[g_i])
                    if value != parent.gene[g_i]:
                        is_valid = True
                # 
                gene_value_list.append(value)
            
            # 开始进行基因变异
            child.gene = parent.gene
            child.gene[gene_index_list] = gene_value_list
            # 评价个体
            self._evaluate_ind(ind = child, param = parent.param)
        
        for c_i in range(self.offsprint_num):
            mutation(parent = parent, child = self.children[c_i])
            # 如果是同步更新
            if is_synchronous and self.children[c_i].fitness < parent.fitness:
                parent.gene = self.children[c_i].gene
                parent.fitness = self.children[c_i].fitness
        # best = self.select_best(self.children)
        # return self.select_best(self.children)
    

    # 单个体的多基因之间的交换
    def _swap_operation(self, parent: Individual, child: Individual, k = 2, is_synchronous = False):
        # 判断 基因i 是否可以和 基因j 交换
        def is_valid_gene_value(ind: Individual, gene_index: int, gene_index_list = None):
            '''
            判断 gene_index 基因座 是否 可以变成 gene_value
            '''
            if gene_index_list == []:
                return True
            
            # 判断 基因i 是否已经在 交换列表中
            if gene_index in gene_index_list:
                return False
            
            # 判断 这个位置上的基因 是否可以和 前一个位置上的基因 交换
            # 判断 i 和 j 是否可以交换
            gene_value = ind.gene[gene_index]
            bound = ind.bounds[gene_index_list[-1]]
            # 判断 gene_index 基因座上是否可以 可以和
            if gene_value not in bound:
                return False
            # 判断要交换的两个基因是否一样
            if gene_value == ind.gene[gene_index_list[-1]]:
                return False
            # 通过 检验
            return True
        
        # 执行交换操作
        def swap(parent: Individual, child: Individual, k = 2):
            child.gene = copy.deepcopy(parent.gene)
            gene_index_list = []
            # 对 k 个基因进行随机变异
            for i in range(k):

                is_valid_gene = False
                while not is_valid_gene:
                    # 随机选择一个基因座
                    gene_index = random.randint(0, parent.gene_num - 1)
                    # 判断
                    is_valid_gene = is_valid_gene_value(ind = parent, 
                                                        gene_index = gene_index, 
                                                        gene_index_list = gene_index_list)
                
                # 记录基因座信息和基因信息
                gene_index_list.append(gene_index)
            
            # 开始交换生成子代
            for i in range(k - 1):
                gene_i_index = gene_index_list[i]
                gene_j_index = gene_index_list[i + 1]
                child.gene[gene_i_index], child.gene[gene_j_index] = child.gene[gene_j_index], child.gene[gene_i_index]
            
            # 计算适应度值
            self._evaluate_ind(ind = child, param = parent.param)
            # pass
        
        # 执行交换操作
        if k < 2:
            raise ValueError(f'基因交换个数k(={k})小于2')
        
        # 生成子代
        for i in range(self.offsprint_num):
            swap(parent = parent, child = self.children[i], k = k)

            # 如果是同步更新
            if is_synchronous and self.children[i].fitness < parent.fitness:
                parent.gene = self.children[i].gene
                parent.fitness = self.children[i].fitness

        # return self.select_best(self.children)

    # 挑选一个个体
    def select_best(self, pop: list, offsprint_num = None):
        if offsprint_num == None:
            offsprint_num = self.offsprint_num
        pop_fitness = [pop[i].fitness for i in range(len(pop))]
        best_index = pop_fitness.index(min(pop_fitness))
        return pop[best_index]

    def output_log(self, g, output_log_path: str):
        with open(output_log_path, 'a') as f:
            solver_info = f'g: {g}; '
            solver_info = solver_info + f'fit: {self.pop[0].fitness}; '
            solver_info = solver_info + ','.join(map(str, list(self.pop[0].gene))) + '; \n'
            f.write(solver_info)
            print(solver_info)

    def _evaluate_ind(self, ind, param):
        '''
        评价一个个体
        '''
        gene_str = ','.join(map(str, list(ind.gene)))
        if gene_str in self.history.keys():
            ind.fitness = self.history[gene_str]
        else:
            ind.param = param
            ind.fitness = ind.fitness_func(ind)
            # del ind.param
            self.history[gene_str] = ind.fitness
        pass

    # 开始求解
    def solver(self, generation = 500, output_log_path = './log.txt'):
        # 初始化log
        if os.path.exists(output_log_path):
            os.remove(output_log_path)
        # 计算初始解评价值
        self._evaluate_ind(ind = self.pop[0], param = self.pop[0].param)
        self.output_log(0, output_log_path)
        # 开始迭代
        # self._swap_operation(parent = self.pop[0], child = self.children, is_synchronous = True)
        for g in range(generation):
            operation_index = random.randint(0, 1)
            if operation_index == 0:
                self._swap_operation(parent = self.pop[0], child = self.children, is_synchronous = True)
            elif operation_index == 1 or sum(self.pop[0].gene) == self.pop[0].gene_num:
                self._mutation_operation(parent = self.pop[0], children = self.children, is_synchronous = True)
            # 记录每次迭代的信息
            self.output_log(g + 1, output_log_path)
            with open('./ind_history.json', 'w') as f:
                history = sorted(self.history.items(), key = lambda x: x[1])
                f.write(json.dumps(history))
        pass

if __name__ == "__main__":
    tmppop = []
    for i in range(5):
        ind = Individual(i, [1,2,3,4], [True] * 4, [[6,2,3]] * 4, name = f'{i}, {i}')
        tmppop.append(ind)
    # pop = Population(tmppop, 0)
    ns = NeighbourhoodSearch(pop = tmppop, offsprint_num = 0)