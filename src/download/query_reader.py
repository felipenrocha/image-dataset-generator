# module to get querie values

with open("../../queries.txt", 'r') as file:
    data = file.readlines()



class Queries:
    # instance attribute
    def __init__(self):

        strings = []
        self.queries = []
        for line in data:
            if line[0] != '#' and line[0] != '\n':
                strings.append(line)
        for line in strings:
            query = self.getQuery(line)
            #unwanted tags
            un_tags = self.getUnwantedTags(line)
            un_tags = list(filter(lambda x: x != '', un_tags)) # remove empty strings
            query = {'name': query, 'unwanted_tags': un_tags}
            self.queries.append(query)
        print(self.queries)
    
    def getQueries(self):
        return self.queries
    def getQuery(self, line):
        i = 0
        query = ''
        while line[i] != ')':
            if line[i] != '+' and line[i] != '(':
                query += line[i]
            i += 1
        return query

    def getUnwantedTags(self,line):
        i = 0
        un_tag_string = ''
        while line[i] != '-':
            i += 1
        while line[i] != ')':
            if line[i] != '-' and line[i] != '(':
                un_tag_string += line[i]
            i += 1
        # create list
        un_tag = []
        word = ''
        i = 0
        while i < len(un_tag_string):
            if un_tag_string[i] == ' ' or un_tag_string[i] == ')':
                un_tag.append(word)
                word = ''
            else:
                word += un_tag_string[i]
            i+=1


        return un_tag


