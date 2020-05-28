# Imports
import numpy as np
import pandas as pd

# Define Options
pd.set_option('max_colwidth',20)

# Function Definitions
def med_list_define():
	list = [
	['Zyrtec','z[eyr][ry]te[ck]|cetirizine'],
	['Singulair','singulai?r|montelu[kc]ast'],
	['Claritin','clarit[ia]n|alavert|loratadine'],
	['Vyvanse','v[yi]van[sc]e?|lisdexamfetamine'],
	['Concerta','conc?erta|Methyl?phenidate|Ritalin|contempla|jornay|adhansia|aptensio|methylin'],
	['Allegra','allegra|fexofenadine'],
	['Flonase','flonase|fluticasone'],
	#mometason is in both Nasonex(nasal) and Asmanex (inhalation)
	['Nasonex','nasonex'],
	['Advair','advair'],
	['Benadryl','ben[ae]dr[iy]l'],
	['Albuterol','albuterol|pro[ -]?air|Ventolin|proventil|accuneb'],
	['Focalin','focalin|de[xzc]methyl?phenidate'],
	['Flovent','flovent|fluticasone'],
	['Melatonin','melatonin'],
	['Intuniv','intuniv|guanfacine'],
	['Ibuprofen','advil|ibuprof[ie]n|Motr[ie]n'],
	['Zoloft','zoloft|sertraline'],
	['Adderall','adderall'],
	['Strattera','stratt?err?a|atomoxetine'],
	['Xyzal','xyzal'],
	['Qvar','qvar|beclomethasone'],
	['Xopenex','Xopenex|levalbuterol'],
	['Symbicort','Symbicort'],
	['Miralax','Miralax'],
	['Clonidine','Clonidine|catapres|kapvay'],
	['Fluoxetine','Fluoxetine|prozac|sarafem'],
	['Desmopressin','Desmopressin|ddavp|nocdurna'],
	['Lexapro','Lexapro|escitalopram'],
	['Abilify','Abilify|aripiprazole'],
	['Nasacort','Nasacort|triamcinolone'],
	['Acetaminophen','Tylenol|acetaminophen'],
	['Prevacid','Prevacid'],
	['Inhaler','Inhaler'],
	['Veramyst','Veramyst'],
	['Vayarin','Vayarin|fish oil'],
	['Dulera','Dulera'],
	['Risperidone','Risperidone'],
	['Synthroid','Synthroid'],
	['Epi Pen','Epi[ -]?Pen']
	]
	return list
def print_num_column(df):
	print("\n# of columns: ",len(df.columns)
		)
def print_notmatch_match_percent(not_match,match):
	percent_matched = match/(not_match+match)
	print('\nNot Matched: {0:,}'.format(not_match))
	print('Matched: {0:,}'.format(match))
	print('Percent Matched: {0:.2%}'.format(percent_matched))
	print()

# Import csv, drop rows without medication name and reset index
data = pd.read_csv(
	'medication_list.csv',
	encoding ='utf-16',
	header=0, sep='\t',
	names = ['dose','form_id','medication_id','medication','reason','when_taken','other_info']
	)
data = data.dropna(subset=['medication']).reset_index(drop=True)

# Call list of Regex terms using function
for x in med_list_define():
	# Create dataframe column if data.medication contains each medication in list
	data[x[0]] = data.medication.str.contains(x[1],case=False)

# Create dataframe with matching/not matching
print_num_column(data)

medication_columns = data.iloc[:, 7:len(data.columns)]

data['no_match'] = ~medication_columns.any(axis=1)

number_matched = medication_columns.any(axis=1).sum()

number_not_matched = data.no_match.sum()

#call print function defined at top
print_notmatch_match_percent(number_not_matched,number_matched)

# Calculate number of times drug has been matched in data.medication
drug_sums = medication_columns.select_dtypes(pd.np.bool).sum().rename('total').sort_values(ascending=False)

# Calculate the percentage of total matches contain this drug name
percent_matched_by_drug = (drug_sums/number_matched).rename('percent')

# Concatenate sums and percent in 1 dataframe
sums_and_percents = pd.concat([drug_sums,percent_matched_by_drug],axis=1) # Work on styling this in the future as %

print('-------------------\nMedication Counts and Percentages\n',sums_and_percents)

print("\n",drug_sums.describe(),"\n")

# Find the top 25 unmatched drugs remaining
top_unmatched = data[data.no_match==1].groupby(['medication'])['medication'].count().sort_values(ascending=False)

print('-----------------\nTop 25 Unmatched Medications\n')

print(top_unmatched[:25])

#How to print and search for particular drug
#print(data[data.medication.str.contains('fish oil',case=False)])

# How to print if particular column is true (search for false positives)
#print(data[data.Concerta==True])
