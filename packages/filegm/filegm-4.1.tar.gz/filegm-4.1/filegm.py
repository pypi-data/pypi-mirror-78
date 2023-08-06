#!python


# --------------------------

import os, shutil, sys
from datetime import datetime, timedelta

# --------------------------					# generator of all files in all folders in the home directory



def pth_gen():
    for root, dirct, filename in os.walk(os.environ['HOME']):
        for file in dirct:
            os.path.join(root,file)
        for name in filename:
            yield os.path.join(root,name)

# ----------------
# ----------------						# time frame input and timestamp conversion



inp = input('Enter the date from which you want to know the files created in this format "Y-M-D": ')

tme = datetime.strptime(inp, "%Y-%m-%d")

tme_tms = datetime.timestamp(tme)

# ----------------
# ----------------						# input according to time frame



inp_2 = input('If you want to limit the time span to a second term after the first, type the second date in the format "Y-M-D", otherwise press the enter key to set the second term to today\'s date: ')


if inp_2:

    if inp_2 == inp:

        tme_2 = datetime.strptime(inp_2, "%Y-%m-%d") + timedelta(days=1)

        tme_tms_2 = datetime.timestamp(tme_2)

    else:

        tme_2 = datetime.strptime(inp_2, "%Y-%m-%d")

        tme_tms_2 = datetime.timestamp(tme_2)

# ----------------
# ----------------



print('\nTotal files in the "home" folder and subfolders:\t\t\t\t\t %d\n' % len([i for i in pth_gen()]))

# ----------------						# extension(s) input
								# generator of all files in all folders of the home with the specified extension(s)


inp_3 = [i for i in input('Specifies the file format, for example ".txt". If more than one format is specified, DO NOT use commas or other punctuation: ').split()]

inp_3_tpl = tuple(inp_3)

def gen_ext():
    for i in pth_gen():
        if i.endswith(inp_3_tpl):
            yield i

# ----------------



ext_lst = []

for i in inp_3_tpl:
    ext_lst.append(i)

print('\nTotal files in the %s format present in the "home" folder and subfolders:\t\t %d\n' % (ext_lst, len([i for i in gen_ext()])))

# ----------------						# mapping, through dictionary, of the filepath (key) with specific extension and the time (value) in which they were created in the computer



m_time = {i: os.path.getmtime(i) for i in gen_ext()}

# ----------------						# first generator: mapping values (time)
								# second generator: values (time) limited to the time period in question
								# list containing all the elements in the period of time in question

def gen_values():
    for i in m_time.values():
        yield i

def gen_values_tme():
    for i in gen_values():
        if i >= tme_tms:
            yield i

tme_lst = [i for i in gen_values_tme()]

# ----------------						# generator value according to the time period in question
								# list containing all the elements in the period of time in question


if inp_2:
    
    def gen_values_tme_2():
        for i in tme_lst:
            if i < tme_tms_2:
                yield i

    tme_2_lst = [i for i in gen_values_tme_2()]

# ----------------						# first generator: tuple (key, value) of the mapping of all files with specific extension and time in question
								# second generator: mapping values (time)
								# third generator: mapping (filepath) keys on the basis of the second generator
								# list of filepath (keys) in question
file_in_focus = []

if inp_2:

    def gen_tpl_lst_a_b():
        for i in m_time.items():
            yield i

    def gen_fcs_tpl_a_b():
        for i in gen_tpl_lst_a_b():
            if i[1] in tme_2_lst:
                yield i

    def gen_file_in_focus_a_b():
        for i in gen_fcs_tpl_a_b():
            yield i[0]

    file_in_focus = [i for i in gen_file_in_focus_a_b()]

else:

    def gen_tpl_lst():
        for i in m_time.items():
            yield i

    def gen_fcs_tpl():
        for i in gen_tpl_lst():
            if i[1] in tme_lst:
                yield i

    def gen_file_in_focus():
        for i in gen_fcs_tpl():
            yield i[0]

    file_in_focus = [i for i in gen_file_in_focus()]

# ----------------						# first generator: split filename from the list of filepath in question
								# filename list
								# cycle manufacturer list containing only duplicate filenames
								# cycle manufacturer list containing the entire path of duplicate files
def gen_split_lst():
    for i in file_in_focus:
        yield os.path.split(i)[1]

split_lst = [i for i in gen_split_lst()]


def gen_split_lst():
    for i in split_lst:
        if  split_lst.count(i) > 1:
            yield i
        
split_duplicates = [i for i in gen_split_lst()]


def gen_whole_duplicate():
    for i in file_in_focus:
        if os.path.split(i)[1] in split_duplicates:
            yield i
        
whole_duplicate = [i for i in gen_whole_duplicate()]

whole_duplicate.sort(key=lambda x: os.path.split(x)[1])

# ----------------						# mapping the filepath (key) and size (value) of duplicate files



w_dpl_dmn = {i: os.path.getsize(i) for i in gen_whole_duplicate()}

# ----------------						# list of tuples [filepath, size]



w_dpl_dmn_lst = [i for i in w_dpl_dmn.items()]

# ----------------						# matrix [[tail, size], [head]]



w_splt_mrx = []


for i in range(len(w_dpl_dmn_lst)):
    w_splt_mrx.append([])
    w_splt_mrx[i].append([os.path.split(w_dpl_dmn_lst[i][0])[1], w_dpl_dmn_lst[i][1]])
    w_splt_mrx[i].append([os.path.split(w_dpl_dmn_lst[i][0])[0]])

# ----------------						# list of lists [tail, size]



sp_sz_lst = []

for i in w_splt_mrx:
    sp_sz_lst.append(i[0])

# ----------------						# list of tuples (tail, size)



sp_sz_tp_ls = []

for i in sp_sz_lst:
    sp_sz_tp_ls.append(tuple(i))

# ----------------						# list of duplicate tuples (tail, size)



dpl_sp_sz_tpl_lst = []

unique = set(sp_sz_tp_ls)

for i in unique:
    count = sp_sz_tp_ls.count(i)
    if count > 1:
        dpl_sp_sz_tpl_lst.append(i)

# ----------------						# list of duplicate lists [tail, size]



dpl_sp_sz_lst = []

for i in range(len(dpl_sp_sz_tpl_lst)):
    dpl_sp_sz_lst.append([])
    dpl_sp_sz_lst[i].append(dpl_sp_sz_tpl_lst[i][0])
    dpl_sp_sz_lst[i].append(dpl_sp_sz_tpl_lst[i][1])

# ----------------						# list of all duplicate paths



join_lst = []

for i in w_splt_mrx:
    if i[0] in dpl_sp_sz_lst:
        join_lst.append(os.path.join(i[1][0], i[0][0]))

join_lst.sort(key=lambda x: os.path.split(x)[1])

# ----------------						# matrix representation of duplicate filepath sorted by filename



mrx_str = []
spltxt_tpl_lst = []
spltxt_tpl_lst_mrx = []
spl_spltxt_lst = []
dpl_prognumeric_lst = []


if len(join_lst) > 0:
    print('\n\nIn the date search, %d duplicate files were found. \v\rYou can choose to delete all of them automatically, or some or none.' % len(join_lst))


    inp_opts = input('If you want to choose between the duplicates which are to be deleted then press "c", if you want to copy them all press "a", otherwise press the "enter" key to automatically omit all duplicates: ')

    if inp_opts == 'c':						# choosing which duplicate files to remove from the list

        dpl_lst = []
        for i in range(len(join_lst)):
            dpl_lst.append([])
            dpl_lst[i].append(join_lst[i])
            dpl_lst[i].append(os.path.split(join_lst[i])[1])

        dpl_lst.sort(key=lambda x: x[1])

        print('\nChoose from the following duplicate items to delete from the list for copying:\n ')
        for i in range(len(dpl_lst)):
            print(i,'\t', dpl_lst[i], end=" ")
            print()
        
        inp_sclt = [i for i in input('\nSelect from the column on the left only one or more of the numbers corresponding to the files you wish to omit from the list for copying, in the case of a multiple selection specify the numbers separated only by a blank space, for example "1 2 3": ').split()]

        inp_sclt_2 = set()
        
        for i in inp_sclt:
            inp_sclt_2.add(int(i))

        dpl_lst_2 = [j for i, j in enumerate(dpl_lst) if i not in inp_sclt_2]	# list comprehension for entering the numbers of multiple items to be removed and efficient remake of the list

        print('\nThis is the new list of duplicate items to copy:\n ')
        for i in range(len(dpl_lst_2)):
            print(i,'\t', dpl_lst_2[i], end=" ")
            print()

								# list system to disassemble the original path and reassemble it with progressive number at the end of the path (before extension)


        for i in dpl_lst_2:
            mrx_str.append(i[0])

        for i in mrx_str:
            spltxt_tpl_lst.append(os.path.splitext(i))

        for i in spltxt_tpl_lst:
            spltxt_tpl_lst_mrx.append(list(i))


        for i in spltxt_tpl_lst_mrx:
            spl_spltxt_lst.append(os.path.split(i[0])[1])


        unique = set(spl_spltxt_lst)

        for i in unique:
            count = spl_spltxt_lst.count(i)
            if count > 1:
                a = -1

                for j in spltxt_tpl_lst_mrx:
                    if os.path.split(j[0])[1] == i:
                        file_in_focus.remove(j[0]+j[1])
                        a += 1
                        dpl_prognumeric_lst.append([j[0] + j[1], os.path.split(j[0])[1] + '_' + str(a) + j[1]])

								# system identical to the one above, but based on the choice "a" to copy all the duplicates, then to number them progressively.

    elif inp_opts == 'a':

        dpl_lst = []
        for i in range(len(join_lst)):
            dpl_lst.append([])
            dpl_lst[i].append(join_lst[i])
            dpl_lst[i].append(os.path.split(join_lst[i])[1])

        dpl_lst.sort(key=lambda x: x[1])


        mrx_str = []
        spltxt_tpl_lst = []
        spltxt_tpl_lst_mrx = []
        spl_spltxt_lst = []
        dpl_prognumeric_lst = []


        for i in dpl_lst:
            mrx_str.append(i[0])

        for i in mrx_str:
            spltxt_tpl_lst.append(os.path.splitext(i))

        for i in spltxt_tpl_lst:
            spltxt_tpl_lst_mrx.append(list(i))


        for i in spltxt_tpl_lst_mrx:
            spl_spltxt_lst.append(os.path.split(i[0])[1])


        unique = set(spl_spltxt_lst)

        for i in unique:
            count = spl_spltxt_lst.count(i)
            if count > 1:
                a = -1

                for j in spltxt_tpl_lst_mrx:
                    if os.path.split(j[0])[1] == i:
                        file_in_focus.remove(j[0]+j[1])
                        a += 1
                        dpl_prognumeric_lst.append([j[0] + j[1], os.path.split(j[0])[1] + '_' + str(a) + j[1]])

# ----------------						# representation of the number of all found files and files found according to each extension



file_in_focus.sort()

if len(file_in_focus) == 0:
    print('\nNo files was found\n')
    sys.exit()
elif len(file_in_focus) == 1:
    print('\nOnly one file was found')
elif len(file_in_focus) > 1:
    print('\nFound %d files ' % len(file_in_focus))

for i in inp_3_tpl:
    a = [j for j in file_in_focus if j.endswith(i)]
    print('of which\t %d\t with "%s" extension' % (len(a), i))

# ----------------						# input for choice: continue or not to copy files
								# creation of the folder and copying of the files inside it, with any progressively numbered duplicates



inp_cnt = input('\nIf you want to create a folder with a copy of these files type "y", otherwise press the "enter" key: ')

print()

if inp_cnt == 'y':

    if len(file_in_focus) > 0:
        path = "%s/%s_%s" % (os.getcwd(),tme, ext_lst)
        os.mkdir(path)
        for i in file_in_focus:
            shutil.copy2(i, path, follow_symlinks=True)

        if len(dpl_prognumeric_lst) > 0:
            for i in dpl_prognumeric_lst:
                shutil.copy2(i[0], path+'/'+i[1], follow_symlinks=True)
                print('Duplicates\t',path+'/'+i[1])

    else:
        sys.exit()

else:
    sys.exit()

# ----------------						# generator of all filenames with local path copied in the destination folder
								# list of all files copied to the destination folder
								# list of the split of only filenames of all files copied in the destination folder

def gen_dest_itm():
    for root, dirct, filename in os.walk(path):
        for file in dirct:
            os.path.join(root,file)
        for name in filename:
            yield (os.path.join(root,name))

crt_prd = []
crt_prd = [i for i in gen_dest_itm()]
crt_prd_split = [os.path.split(i)[1] for i in crt_prd]

# ----------------						# representation of the possible difference in the quantity of files in the source list and in the destination folder



difference = []

if len(file_in_focus) == len(crt_prd):
    print('\nThe list and the folder under examination have the same number of items.')
else:
    print('\nThe destination folder contains %d files, so there is a %d file gap between the source list and the destination folder. If the number is negative this means that there are more files copied than the source list, this probably depends on the copying of duplicate files. if the number is positive this may depend on duplicate files but also on other causes, for example symbolic links.' % (len(crt_prd), len(file_in_focus)-len(crt_prd)))

# ----------------						# input whether or not to delete the destination folder of the copied files



print('\nThe folder\t " %s "\t has been generated in the current directory.' %path)
a = input('\nDo you want to delete the newly created folder containing the copy of the files? (answer y or n) ')

if a=='y':
    shutil.rmtree(path)
else:
    sys.exit()









