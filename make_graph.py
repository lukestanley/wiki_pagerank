#!/usr/bin/python
from re import finditer
from cPickle import load
from os import system as run

def process_line(line, d, outfile):
    ''' 
    Prints outlinks for each page.

    Example contents of line: 
    ...',5),(12,0,'A._S._Neill',3),(12,0,'AK_Press',4),(12,0,...

    Each tuple is of the form ('from' page, namespace, 'to' page).  Print a
    line for each 'from' page with the outlinks that are in namespace 0 (the
    main wikipedia, ignores 'talk' pages, etc). Annoyingly, the 'from' pages
    are given by ID and the 'to' pages by name. Use the dictionary d to map the
    text names to IDs for consistency (and some space savings).  
    '''
    pattern = "\((\d+),(\d+),'(.*?)',(\d+)\)[,;]"
    current_page = None
    for match in finditer(pattern, line):
        from_page, namespace, to_page, from_ns = match.groups()
        if from_page != current_page: 
            if current_page: outfile.write('\n') # new line for all but the first
            outfile.write(from_page + ' ')
            current_page = from_page
        if namespace == '0' and to_page in d: outfile.write(str(d[to_page]) + ' ')

def main():
    ''' Reads pagelinks.sql line by line and processes it. Needs the pickled 
    dictionary mapping page names to IDs '''
    print "building the graph..."
    crap = 'INSERT INTO `pagelinks` VALUES'
    path = ''#set if needed (different current dir)
    pickle = 'title-ID_dict.pickle'
    d = load(open(path+pickle))
    with open('graph.txt', 'w') as outfile:
        for line in open('pagelinks.sql'):
            if line[:len(crap)] == crap: 
                process_line(line, d, outfile)
    
    run('wc -l graph.txt > graph.txt.wc')

if __name__ == "__main__":
    main()
