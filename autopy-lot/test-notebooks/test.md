---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.0
  kernelspec:
    display_name: Python 3
    name: python3
---

<!-- #region id="VS_EDvAXXlCq" colab_type="text" -->
# Initialization
<!-- #endregion -->

```python id="erUvXpQHXntK" colab_type="code" outputId="90803cc5-5a16-43ad-eaf8-6c74b1a003f2" colab={"base_uri": "https://localhost:8080/", "height": 35}
from google.colab import drive
drive.mount('/gdrive')
import matplotlib.pyplot as plt
```

<!-- #region id="ZhUvOQAI5Tl3" colab_type="text" -->
# Boyer Moore Algorithm | Good Suffix heuristic
**DESCRIPTION**

In computer science, the Boyer–Moore string-search algorithm is an efficient string-searching algorithm that is the standard benchmark for practical string-search literature. It was developed by Robert S. Boyer and J Strother Moore in 1977. The algorithm preprocesses the string being searched for (the pattern), but not the string being searched in (the text). It is thus well-suited for applications in which the pattern is much shorter than the text or where it persists across multiple searches. The Boyer–Moore algorithm uses information gathered during the preprocess step to skip sections of the text, resulting in a lower constant factor than many other string search algorithms. In general, the algorithm runs faster as the pattern length increases. The key features of the algorithm are to match on the tail of the pattern rather than the head, and to skip along the text in jumps of multiple characters rather than searching every single character in the text. 

**PERFORMANCE**

The Boyer–Moore algorithm as presented in the original paper has worst-case running time of **`O(n+m)`** only if the pattern does not appear in the text. **`here we gurantee that the patterns always exist, so it never reach the worst case scenario `**
<!-- #endregion -->

```python id="FKI3rL-x7ol7" colab_type="code" colab={}
# Python3 program for Boyer Moore Algorithm with 
# Good Suffix heuristic to find pattern in 
# given text string 

# preprocessing for strong good suffix rule 
def preprocess_strong_suffix(shift, bpos, pat, m): 

	# m is the length of pattern 
	i = m 
	j = m + 1
	bpos[i] = j 

	while i > 0: 
		
		'''if character at position i-1 is 
		not equivalent to character at j-1, 
		then continue searching to right 
		of the pattern for border '''
		while j <= m and pat[i - 1] != pat[j - 1]: 
			
			''' the character preceding the occurrence 
			of t in pattern P is different than the 
			mismatching character in P, we stop skipping 
			the occurrences and shift the pattern 
			from i to j '''
			if shift[j] == 0: 
				shift[j] = j - i 

			# Update the position of next border 
			j = bpos[j] 
			
		''' p[i-1] matched with p[j-1], border is found. 
		store the beginning position of border '''
		i -= 1
		j -= 1
		bpos[i] = j 

# Preprocessing for case 2 
def preprocess_case2(shift, bpos, pat, m):
	j = bpos[0] 
	for i in range(m + 1): 
		
		''' set the border position of the first character 
		of the pattern to all indices in array shift 
		having shift[i] = 0 '''
		if shift[i] == 0: 
			shift[i] = j 
			
		''' suffix becomes shorter than bpos[0], 
		use the position of next widest border 
		as value of j '''
		if i == j: 
			j = bpos[j] 

'''Search for a pattern in given text using 
Boyer Moore algorithm with Good suffix rule '''
def BMPsearch_good(pat, text):
  pos = []
  s = 0
  m = len(pat) 
  n = len(text) 

  bpos = [0] * (m + 1) 

  # initialize all occurrence of shift to 0 
  shift = [0] * (m + 1) 

  # do preprocessing 
  preprocess_strong_suffix(shift, bpos, pat, m) 
  preprocess_case2(shift, bpos, pat, m) 

  while s <= n - m: 
    j = m - 1

    ''' Keep reducing index j of pattern while characters of 
      pattern and text are matching at this shift s'''
    while j >= 0 and pat[j] == text[s + j]: 
      j -= 1
      
    ''' If the pattern is present at the current shift, 
      then index j will become -1 after the above loop '''
    if j < 0: 
      #print("pattern occurs at shift = %d" % s)
      pos.append(s)
      s += shift[0] 
    else: 
      
      '''pat[i] != pat[s+j] so shift the pattern 
      shift[j+1] times '''
      s += shift[j + 1]
  return pos
```

<!-- #region id="x1U1Flj-YCmW" colab_type="text" -->
# Necessary Functions
<!-- #endregion -->

```python id="8YN97agpYGx9" colab_type="code" colab={}
from collections import OrderedDict

########################################################################


def find_repeats( dna, n):
    """
    This help function for repeats_identifier find and count repeats for 
    each dna sequence
    dna: sequence, string
    n: number of repeats, int
    """
    repeats = {}
    for i in range(0, len(dna)):
        repeat = dna[i:i+n] # generate possible repeats
        if len(repeat) == n:
            if repeat not in repeats:
                repeats [repeat] = 1 # initiate record
            else:
                # count repeated repeats
                repeats[repeat] = repeats.get(repeat) + 1
    return dict(sorted(repeats.items()))



####################################################################

def get_unique_patterns(dna,n):
  repeats = []
  for i in range(0, len(dna)):
    repeat = dna[i:i+n] # generate possible repeats
    if len(repeat) == n:
         repeats.append(repeat)
  return sorted(list(dict.fromkeys(repeats))) #eliminate duplicates

########################################################


def get_repeats_with_loc(dna,n):
  # get a sorted list of unique patterns
  patterns = get_unique_patterns(dna,n)
  #create a dictionary with pattern and its loc in the list
  patterns_loc = {}
  # to hold actual loc
  locs = []
  for k in range(0,len(patterns)):
    locs.append([])

  for i in range(0,len(patterns)):
    patterns_loc[patterns[i]] = i #insert the loc

  print(patterns_loc)
  # now actually including all the locs
  for i in range(0,len(dna)):
    repeat = dna[i:i+n]
    if len(repeat)==n:
      # get the location (where to be inserted in the pattern_loc) of the pattern just found
      arr_loc = patterns_loc[repeat]
      # print("arrloc{}".format(arr_loc))
      # include the actual location of occurance in dna
      locs[arr_loc].append(i)

  #returns the loc of each unique pattern as an array of array
  return locs

%matplotlib inline



####################################################

def plot_pattern_distr_by_frq(dna):
  codon_repeats = find_repeats(dna,3)
  codon_repeats = {k: v for k, v in sorted(codon_repeats.items(), key=lambda item: item[1])}
  frq = list(codon_repeats.values())
  seq_x = list(codon_repeats.keys())
  
  fig = plt.figure(figsize=[4,4])

  plt.bar(seq_x,frq,width=0.5,color='g')
  plt.ylabel('frequency')
  plt.title("CODON DISTRIBUTION - sorted: frqncy")
  plt.show() 



######################################################3


def percent_of_occurence(seq):
  repeats_ = find_repeats(seq,3)
  total_occur = 0
  percent_dist = {}
  for rpt in repeats_:
    total_occur += repeats_[rpt]
  # print("total",total_occur)
  for rpt in repeats_:
    percent_dist[rpt] = (repeats_[rpt]/total_occur)*100
  percents = [ per for per in percent_dist.values() ]
  return percent_dist,percents


######################################################

def print_pattern_wise_locs(patterns,locs):
  patterns = patterns
  locs = locs
  for i in range(0,len(patterns)):
    print("Patterns:    {} | length: {} | loc: {}".format(patterns[i],len(locs[i]),locs[i]))



################## common patterns in individual files

from os import listdir
from os.path import isfile, join

def helper_funtion(my_path,length):
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    file_names = []

    for file_ in only_files:
      file_path = my_path+'/'+file_
      file_names.append(file_.split('.txt')[0])

      with open(file_path,'r') as file:
        content = file.readlines()[0]
        patterns = get_unique_patterns(content,length)
        print(file_ + " : patterns count: "+str(len(patterns)))

################# common patterns considering all files
def helper_function_2(my_path,length):
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    file_names = []
    patterns = []
    for file_ in only_files:
      file_path = my_path+'/'+file_
      file_names.append(file_.split('.txt')[0])

      with open(file_path,'r') as file:
        content = file.readlines()[0]
        temp_patterns = get_unique_patterns(content,length)
        patterns.append(temp_patterns)

    common_patterns = set(patterns[0]) # convert this to a set 
    for i in range(0,len(patterns)):
      common_patterns = common_patterns & set(patterns[i]) # intersection of sets, holds only common elements if any
    print("common patterns count: "+ str(len(common_patterns)) + " : "+str(list(common_patterns)))
        
###########################
from time import process_time 

def common_loc_pattern(patterns,path):
  # examine each patterns seperately
  for pat in patterns:
    com_pos = [] # holds the global array of locations for a pattern
    my_path = path
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    file_names = []

    for file_ in only_files:
      file_path = my_path+'/'+file_
      file_names.append(file_.split('.txt')[0])

      with open(file_path,'r') as file:
        content = file.readlines()[0]
        t=process_time() # start time
        res = BMPsearch_good(pat,content)
        com_pos.append(res) # include the resultant array
        elapsed_time = process_time()-t # elapsed time in seconds

        # uncomment the below line to see the locations
        #print(str(res))

    common_loc = set(com_pos[0]) # convert this to a set 
    for i in range(0,len(com_pos)):
      common_loc = common_loc & set(com_pos[i]) # intersection of sets, holds only common elements if any
    print(pat+ ": common locs: "+ str(list(common_loc)))



##################
def find_repeats( data, n):
    """
    This help function for repeats_identifier find and count repeats for 
    each dna sequence
    dna: sequence, string
    n: number of repeats, int
    """
    repeats = {}
    for i in range(0, len(data)):
        repeat = data[i:i+n] # generate possible repeats
        if len(repeat) == n:
            if repeat not in repeats:
                repeats [repeat] = 1 # initiate record
            else:
                # count repeated repeats
                repeats[repeat] = repeats.get(repeat) + 1
    return dict(sorted(repeats.items()))


#######################
def helper_function_3(path):
  my_path = path
  only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
  file_names = []

  for file_ in only_files:
    file_path = my_path+'/'+file_
    file_names.append(file_.split('.txt')[0])

    with open(file_path,'r') as file:
      content = file.readlines()[0]
      res = find_repeats(content,1) 
      print(file_+" : "+ str(res))


def helper_function_4(path,len):
  my_path = path
  only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
  file_names = []

  for file_ in only_files:
    file_path = my_path+'/'+file_
    file_names.append(file_.split('.txt')[0])

    with open(file_path,'r') as file:
      content = file.readlines()[0]
      codon_repeats = find_repeats(content,len)
      codon_repeats = {k: v for k, v in sorted(codon_repeats.items(), key=lambda item: item[0])}
      frq = list(codon_repeats.values())
      seq_x = list(codon_repeats.keys())
      
      fig = plt.figure(figsize=[6,5])
      print(file_)
      plt.bar(seq_x,frq,width=0.5,color='g')
      plt.ylabel('frequency')
      plt.title("CODON DISTRIBUTION - sorted: codon")
      plt.show()  



def helper_function_5(path,len):
  my_path = path
  only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
  file_names = []

  for file_ in only_files:
    file_path = my_path+'/'+file_
    file_names.append(file_.split('.txt')[0])

    with open(file_path,'r') as file:
      content = file.readlines()[0]
      repeats_ = find_repeats(content,len)
      total_occur = 0
      percent_dist = {}
      for rpt in repeats_:
        total_occur += repeats_[rpt]
      # print("total",total_occur)
      for rpt in repeats_:
        percent_dist[rpt] = (repeats_[rpt]/total_occur)*100
      percents = [ per for per in percent_dist.values() ]
      # return percent_dist,percents
      print(file_ + " ----------")
      print(str(percent_dist))
      print("")
      
```

<!-- #region id="YVpYbNbfY_OS" colab_type="text" -->
# DJ1
<!-- #endregion -->

<!-- #region id="Xk8Jw23Wjz5p" colab_type="text" -->
## Unique Patterns
Finding All the unique patterns in each file seperately
<!-- #endregion -->

<!-- #region id="6wdXMOlLZIuZ" colab_type="text" -->
### Find Unique Patterns in all the files with pattern length 3
<!-- #endregion -->

```python id="LL0XGo27ZWjt" colab_type="code" outputId="7f8b759f-e501-4d8d-c1d0-162c0facea2e" colab={"base_uri": "https://localhost:8080/", "height": 0}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',3)
```

<!-- #region id="gA3MRUNAb_oG" colab_type="text" -->
### Find Unique Patterns in all the files with pattern length 4
<!-- #endregion -->

```python id="XWJAERp-cDw-" colab_type="code" outputId="b09d9588-7e41-4558-cb8b-273242f49578" colab={"base_uri": "https://localhost:8080/", "height": 403}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',4)
```

<!-- #region id="0SUEeDCkcT3m" colab_type="text" -->
### Find Unique Patterns in all the files with pattern length 5
<!-- #endregion -->

```python id="1tTsh866cbVo" colab_type="code" outputId="196f3414-8ddb-42d5-97c8-5ec6ae7bbd79" colab={"base_uri": "https://localhost:8080/", "height": 403}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',5)
```

<!-- #region id="ahITbF36dgpY" colab_type="text" -->
### Find Unique Patterns in all the files with pattern length 6
<!-- #endregion -->

```python id="837t20qddjEP" colab_type="code" outputId="c8aea9c2-4375-44a8-868e-08ad161ec36a" colab={"base_uri": "https://localhost:8080/", "height": 0}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',6)
```

<!-- #region id="KHS3CK0vdrfr" colab_type="text" -->
### Find Unique Patterns in all the files with pattern length 7
<!-- #endregion -->

```python id="dXl_rwLfdt1-" colab_type="code" outputId="4bfb416e-79b0-4605-8506-6c2aeb6d88c8" colab={"base_uri": "https://localhost:8080/", "height": 403}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',7)
```

<!-- #region id="88LILsoxdz10" colab_type="text" -->
### Find Unique Patterns in all the files with pattern length 8
<!-- #endregion -->

```python id="mi5CoVd0d3wf" colab_type="code" outputId="08c2f8fa-b4d7-4515-b82c-7f9d106969e6" colab={"base_uri": "https://localhost:8080/", "height": 403}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',8)
```

<!-- #region id="uQC9Zq5bkCv0" colab_type="text" -->
## Common Patterns
Finding those patterns that exist in all the files
<!-- #endregion -->

<!-- #region id="09V0atLPgksh" colab_type="text" -->
### Find common Unique Patterns considering all the files with pattern length 3
<!-- #endregion -->

```python id="z57V6ZYDgtM9" colab_type="code" outputId="40fe8658-6bd6-41ab-f7d0-a56e072cf8a5" colab={"base_uri": "https://localhost:8080/", "height": 0}
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',3)
```

<!-- #region id="LvVR78SzhwQR" colab_type="text" -->
### Find common Unique Patterns considering all the files with pattern length 4
<!-- #endregion -->

```python id="78I3rcW9kHCA" colab_type="code" outputId="3e89e843-bf84-442d-ed9f-a6b4cb351c57" colab={"base_uri": "https://localhost:8080/", "height": 0}
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',4)
```

<!-- #region id="Wvu9uJ3Tqon9" colab_type="text" -->
### Find common Unique Patterns considering all the files with pattern length 5
<!-- #endregion -->

```python id="OOe8TFLZqp-8" colab_type="code" outputId="dca44c02-4063-4211-c2b0-51a00d122805" colab={"base_uri": "https://localhost:8080/", "height": 0}
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',5)
```

<!-- #region id="jKsq8WQbqwCu" colab_type="text" -->
### Find common Unique Patterns considering all the files with pattern length 6
<!-- #endregion -->

```python id="AU0yoEiJqy1m" colab_type="code" outputId="06048ab7-152f-491e-ebe0-385458ceabb0" colab={"base_uri": "https://localhost:8080/", "height": 0}
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',6)
```

<!-- #region id="ArEMGMRushAW" colab_type="text" -->
## Find common locs for each patterns with pattern length 3



<!-- #endregion -->

```python id="RG1vawhxsoqm" colab_type="code" outputId="ff2562bf-5881-4e5c-d649-6d383f7cc0d7" colab={"base_uri": "https://localhost:8080/", "height": 0}
patterns = ['481', '351', '665', '618', '282', '135', '486', '531', '456', '211', '861', '518', '182', '727', '165', '473', '858', '575', '628', '686', '785', '646', '388', '281', '818', '355', '218', '521', '347', '574', '848', '464', '474', '687', '555', '745', '827', '244', '223', '832', '268', '213', '528', '732', '234', '114', '556', '834', '174', '854', '747', '432', '253', '621', '241', '175', '316', '851', '326', '868', '233', '338', '152', '768', '385', '212', '722', '128', '145', '471', '155', '718', '438', '526', '568', '215', '484', '251', '844', '421', '482', '546', '846', '127', '257', '553', '815', '644', '178', '283', '513', '334', '847', '144', '864', '512', '535', '744', '757', '455', '751', '151', '874', '124', '855', '448', '538', '713', '833', '317', '715', '511', '278', '884', '341', '377', '812', '136', '814', '141', '651', '761', '352', '748', '515', '332', '113', '134', '252', '554', '871', '231', '224', '671', '272', '758', '572', '321', '784', '162', '585', '881', '578', '173', '824', '371', '123', '728', '514', '866', '483', '172', '273', '117', '228', '147', '516', '878', '417', '657', '187', '721', '445', '132', '148', '841', '457', '284', '345', '581', '787', '485', '831', '111', '122', '271', '571', '558', '467', '525', '586', '138', '717', '451', '867', '116', '887', '886', '524', '771', '752', '741', '738', '154', '583', '587', '412', '711', '431', '852', '875', '743', '788', '112', '478', '443', '853', '885', '458', '527', '288', '131', '828', '811', '588', '314', '888', '248', '221', '311', '648', '411', '227', '437', '146', '845', '315', '714', '137', '684', '216', '627', '625', '872', '863', '821', '285', '214', '688', '725', '121', '611', '816', '415', '125', '161', '468', '381', '883', '348', '736', '517', '181', '547', '115', '186', '331', '873', '188', '541']
common_loc_pattern(patterns,'/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1')
```

<!-- #region id="2_NXeuLmtLgW" colab_type="text" -->
## Find common locs for each patterns with pattern length 4
<!-- #endregion -->

```python id="dRio4xJgtNCU" colab_type="code" outputId="6e98c88a-cd64-42dd-9354-a3393e52a6d7" colab={"base_uri": "https://localhost:8080/", "height": 237}
patterns = ['8751', '7888', '8788', '8514', '8711', '8511', '4788', '2888', '8878', '8848', '8288', '8881']
common_loc_pattern(patterns,'/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1')
```

<!-- #region id="uR3AjmHYvRRe" colab_type="text" -->
## Codon distribution
Prints the number of occurence of each codon in every file
<!-- #endregion -->

```python id="gM0x75rZvVFB" colab_type="code" outputId="51ffb184-4d2b-46c2-b9a9-6af71ed2c546" colab={"base_uri": "https://localhost:8080/", "height": 403}
helper_function_3('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1')
```

<!-- #region id="M8FAORkO-Qgw" colab_type="text" -->
## Plot codon Distribution 
<!-- #endregion -->

```python id="hP_8CFZ_-VVc" colab_type="code" outputId="16e81737-d1af-4654-f2c5-fcf1c02e6c75" colab={"base_uri": "https://localhost:8080/", "height": 1000}
helper_function_4('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',1)
```

<!-- #region id="mkZ3J5DNA8kY" colab_type="text" -->
## Percentage of each codon
<!-- #endregion -->

```python id="ivu4-sJTBAyJ" colab_type="code" outputId="c740e2d6-7e82-4bc0-9ee3-4809e6b50bc6" colab={"base_uri": "https://localhost:8080/", "height": 1000}
helper_function_5('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_DJ1',1)
```

<!-- #region id="VGm3cV_dFYqC" colab_type="text" -->
# PARKIN
<!-- #endregion -->

<!-- #region id="by_XIo-jFl-y" colab_type="text" -->
## Unique patterns

<!-- #endregion -->

<!-- #region id="sErRrVFJFePB" colab_type="text" -->
### Finding unique patterns with pattern length 3
<!-- #endregion -->

```python id="0ZFBx8-jFu0E" colab_type="code" outputId="9c0b96b3-34be-4ff1-83e4-cce89ee7b57b" colab={"base_uri": "https://localhost:8080/", "height": 917}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',3)
```

<!-- #region id="nk_jZ9uiF5fG" colab_type="text" -->
### Finding unique patterns with pattern length 4
<!-- #endregion -->

```python id="l-U2jwtpF9ZX" colab_type="code" outputId="e20d85e9-386d-41f2-c28e-4961de90c9e5" colab={"base_uri": "https://localhost:8080/", "height": 917}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',4)
```

```python id="9TLLf7P_F_US" colab_type="code" colab={}

```

<!-- #region id="5sDG_CYuGBRd" colab_type="text" -->
### Finding qnique patterns with pattern length 5
<!-- #endregion -->

```python id="hF8NG_c8GGFS" colab_type="code" outputId="540936b9-7bae-40fd-977b-5368e1852be0" colab={"base_uri": "https://localhost:8080/", "height": 917}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',5)
```

<!-- #region id="Zi7moBzTGKbM" colab_type="text" -->
### Finding unique patterns with pattern length 6
<!-- #endregion -->

```python id="m-8C1K4kGQQT" colab_type="code" outputId="61bee587-10ca-4b01-8377-27ff1192d990" colab={"base_uri": "https://localhost:8080/", "height": 917}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',6)
```

<!-- #region id="undRW7SNGTcH" colab_type="text" -->
### Finding uniuqe patterns with pattern length 7
<!-- #endregion -->

```python id="3IBNwFuOGYxi" colab_type="code" outputId="2a0a78bf-b63e-4484-d935-fda8407bea64" colab={"base_uri": "https://localhost:8080/", "height": 917}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',7)
```

<!-- #region id="L-kNe6qnGnO9" colab_type="text" -->
### Finding unique patterns with pattern length 8
<!-- #endregion -->

```python id="UMZIdsnpGsmc" colab_type="code" outputId="9fc59733-70ba-485e-fbae-984804c2f00f" colab={"base_uri": "https://localhost:8080/", "height": 917}
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',8)
```

<!-- #region id="BwjyAJt9GyBw" colab_type="text" -->
## Common patterns
<!-- #endregion -->

<!-- #region id="hq6Ey4tLG9sz" colab_type="text" -->
### Finding common patterns with pattern length 3
<!-- #endregion -->

```python id="6z0alVcTHBmL" colab_type="code" outputId="bc4966c3-8f5e-47b7-fc76-1ed965df5fe6" colab={"base_uri": "https://localhost:8080/", "height": 55}
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',3)
```

<!-- #region id="YTTLaNCWHMJ7" colab_type="text" -->
### Finding common patterns with pattern length 4
<!-- #endregion -->

```python id="iF7LFTItHP5k" colab_type="code" outputId="8c39c5a5-f1f9-4038-de1a-66d1a6895fe0" colab={"base_uri": "https://localhost:8080/", "height": 35}
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',4)
```

<!-- #region id="I_Tp8TZuHVrt" colab_type="text" -->
### Finding common patterns with pattern length 5
<!-- #endregion -->

```python id="UNjaY8NpHZtt" colab_type="code" outputId="e1eab1f6-783b-45b9-ec03-fe17e9fdb4ff" colab={"base_uri": "https://localhost:8080/", "height": 35}
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',5)
```

<!-- #region id="2qInfXXrHj6f" colab_type="text" -->
## Common locs
<!-- #endregion -->

<!-- #region id="w2oIvQYDHnBD" colab_type="text" -->
### common locs with pattern length 3
<!-- #endregion -->

```python id="gyqSdWfmHriO" colab_type="code" outputId="96b9bc62-84e9-4019-a4b6-b4b7a9d621be" colab={"base_uri": "https://localhost:8080/", "height": 1000}
patterns = ['112', '832', '376', '513', '137', '541', '572', '458', '355', '148', '531', '251', '477', '411', '447', '518', '847', '431', '747', '732', '871', '852', '244', '317', '184', '124', '225', '343', '571', '185', '417', '472', '165', '131', '113', '351', '711', '728', '478', '551', '613', '858', '881', '282', '733', '751', '887', '628', '714', '126', '451', '511', '212', '466', '727', '527', '324', '768', '813', '854', '334', '285', '311', '161', '515', '611', '586', '187', '154', '145', '116', '284', '415', '514', '861', '588', '125', '771', '753', '261', '715', '153', '778', '535', '115', '532', '182', '422', '814', '766', '557', '127', '773', '152', '157', '648', '287', '128', '133', '246', '467', '874', '812', '512', '517', '173', '833', '312', '834', '475', '883', '338', '181', '853', '314', '151', '228', '363', '224', '177', '147', '888', '481', '878', '357', '215', '841', '585', '428', '371', '272', '111', '327', '114', '558', '785', '122', '281', '135', '141', '713', '781', '818', '288', '388', '525', '655', '718', '271']
common_loc_pattern(patterns,'/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN')
```

<!-- #region id="QCGF3eDs0Nt-" colab_type="text" -->
### common locs of length 4
<!-- #endregion -->

```python id="bAsB1moa0RL1" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 109} outputId="c98315dc-1070-4a20-e195-a553df75158a"
patterns = ['3111', '1113', '7858', '1125', '8181']
common_loc_pattern(patterns,'/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN')
```

<!-- #region id="qKKn174u1nwL" colab_type="text" -->
## codon distribution

<!-- #endregion -->

```python id="xzCr0QDl1q26" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 937} outputId="d5ccc112-4cf9-4d0f-813a-edb72d210822"
helper_function_3('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN')
```

<!-- #region id="zoOsJH9u16dX" colab_type="text" -->
## plot codon distribution
<!-- #endregion -->

```python id="vUlU7QEC19Iy" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 1000} outputId="c5633ceb-19e7-44eb-f321-9911bb5a9e38"
helper_function_4('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',1)
```

<!-- #region id="UqMgWh232NkG" colab_type="text" -->
## percentage of each codon
<!-- #endregion -->

```python id="UXQq8GW52QaG" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 1000} outputId="cd792b68-6167-4d5b-cc8f-501a5ee992a3"
helper_function_5('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PARKIN',1)
```

<!-- #region id="6J-h86vy4OB_" colab_type="text" -->
# PINK1
<!-- #endregion -->

<!-- #region id="9ykmg5Ut4ZQ0" colab_type="text" -->
## Unique patterns
<!-- #endregion -->

<!-- #region id="RNACcfJo4bY7" colab_type="text" -->
### Finding unique patterns og length 3
<!-- #endregion -->

```python id="GLS6gvT94fjw" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 531} outputId="ddc8e463-4303-45cf-8124-64c6c537372b"
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',3)
```

<!-- #region id="2vtWGjNi4sWO" colab_type="text" -->
### Finding unique patternns of  length 4
<!-- #endregion -->

```python id="zJ1gs3n-4vrN" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 531} outputId="ad1b5e6f-6c95-49c3-d26c-47e5cff3440f"
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',4)
```

<!-- #region id="6OaiixAC4zID" colab_type="text" -->
### Finding unique patterns of length 5
<!-- #endregion -->

```python id="cEjei6LN42f_" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 531} outputId="6ee81dcc-860a-4fc2-a024-6023fb2825af"
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',5)
```

<!-- #region id="E7fOhCV947hE" colab_type="text" -->
###  Finding unique patterns of length 6
<!-- #endregion -->

```python id="DewM4T3n4-15" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 531} outputId="36ee3332-1fd0-4554-b5cb-53a17e6f066b"
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',6)
```

<!-- #region id="7lw94Vh75Dcj" colab_type="text" -->
### Finding unique patterns of length 7
<!-- #endregion -->

```python id="actEkNb45I-g" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 531} outputId="39e30eb7-0d7a-4cc2-b326-d14046b95033"
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',7)
```

<!-- #region id="vXjdV8q05Qzs" colab_type="text" -->
### finding unique patterns of length of 8
<!-- #endregion -->

```python id="-12CcNsP5Vis" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 531} outputId="1ec4e8ee-f885-484e-d668-cf219126418d"
helper_funtion('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',8)
```

<!-- #region id="56z-A5kq5n-Z" colab_type="text" -->
## common patterns
<!-- #endregion -->

<!-- #region id="1Skcx3C85t2j" colab_type="text" -->
### Common patterns of length 3
<!-- #endregion -->

```python id="YCSCIdNe5wzT" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 55} outputId="ea84f849-3adb-41e9-f1b1-11981fd801d9"
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',3)
```

<!-- #region id="3cgwW1YS56gR" colab_type="text" -->
### common patterns of length 4
<!-- #endregion -->

```python id="5zFnz-i259cO" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 35} outputId="0628be76-e798-43c6-84b6-4831538720d5"
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',4)
```

<!-- #region id="oXOR0RmA6DWv" colab_type="text" -->
### common patterns of length 5
<!-- #endregion -->

```python id="iD1Oe9B96GZS" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 35} outputId="8a259836-b147-49d9-f6dd-e8ece949abf9"
helper_function_2('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',5)
```

<!-- #region id="TcsJlles6N9H" colab_type="text" -->
## Common locs
<!-- #endregion -->

<!-- #region id="pwB3kNAn6Siw" colab_type="text" -->
### common locs with pattern length 3
<!-- #endregion -->

```python id="5RNzrt4_6Vyy" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 1000} outputId="990c4ab6-8f79-482f-94dc-612b9fbed769"
patterns = ['111', '728', '571', '533', '715', '858', '871', '134', '612', '215', '475', '178', '428', '317', '787', '228', '347', '355', '225', '733', '887', '127', '271', '513', '881', '861', '143', '281', '581', '572', '115', '152', '541', '731', '851', '645', '278', '246', '746', '527', '145', '588', '882', '518', '485', '711', '261', '414', '727', '282', '716', '751', '146', '481', '784', '785', '886', '363', '244', '874', '532', '684', '713', '722', '732', '768', '114', '767', '818', '585', '883', '841', '147', '137', '153', '847', '154', '781', '477', '448', '165', '131', '854', '514', '311', '157', '515', '371', '838', '214', '287', '888', '312', '431', '417', '141', '224', '388', '736', '125', '112', '187', '274', '454', '653', '273', '382', '868', '878', '286', '458', '148', '438', '212', '447', '837', '135', '177', '747', '628', '384', '631', '284', '834', '512', '221', '753', '272', '478', '525', '551', '124', '251', '162', '116', '555', '188', '472', '778', '173', '714']
common_loc_pattern(patterns,'/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1')
```

<!-- #region id="l52-5uA26otN" colab_type="text" -->
### common locs with patterns length 4
<!-- #endregion -->

```python id="SMvLouFZ6tSb" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 35} outputId="faace1e3-72df-4c08-baa9-5e86cd923e12"
patterns = ['8883']
common_loc_pattern(patterns,'/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1')
```

<!-- #region id="iu5LZi4V7D4Y" colab_type="text" -->
## codon distribution
<!-- #endregion -->

```python id="h5LEfiAb7Gab" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 531} outputId="d6c5a3bc-16d9-4642-c18c-d09e354fae94"
helper_function_3('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1')
```

<!-- #region id="c2upZkBM7ORR" colab_type="text" -->
## Plot codon distribution
<!-- #endregion -->

```python id="Rx2piH6j7QrO" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 1000} outputId="7e0bbef4-9c92-469b-ebed-86d40bdcc61b"
helper_function_4('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',1)
```

<!-- #region id="YHdWwhds7bHu" colab_type="text" -->
## percentage of each codon
<!-- #endregion -->

```python id="NZKM3ROf7dfO" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 1000} outputId="707c4b34-7561-48f0-c75e-a6aa6f3ef8dc"
helper_function_5('/gdrive/My Drive/Genomics/job/data/Output_RYNUM/RYNUM_output_RY_PINK1',1)
```

<!-- #region id="zgeCiQbm7-KZ" colab_type="text" -->
# CONCLUSION
could not find any common pattern at same location for 3 of the hub genes
<!-- #endregion -->
