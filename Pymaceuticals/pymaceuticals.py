#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Hide warning messages in notebook
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These)
mouse_drug_data_to_load = "data/mouse_drug_data.csv"
clinical_trial_data_to_load = "data/clinicaltrial_data.csv"

# Compare the following drugs
drug_list=['Capomulin', 'Infubinol', 'Ketapril', 'Placebo']
markers=['o','x','d','^']
colors=['green','red','black','blue']

# Read the Mouse and Drug Data and the Clinical Trial Data
mouse_drug_data=pd.read_csv(mouse_drug_data_to_load)
clinical_trial_data=pd.read_csv(clinical_trial_data_to_load)


# Combine the data into a single dataset
clinical_drug_trial_df=pd.merge(clinical_trial_data, mouse_drug_data, how='left', on='Mouse ID')


# Display the data table for preview
clinical_drug_trial_df.head()


# ## Tumor Response to Treatment

# In[2]:


# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint 
drug_timepoint_group=clinical_drug_trial_df.groupby(['Drug','Timepoint'])
mean_tumor_volume=drug_timepoint_group['Tumor Volume (mm3)'].mean()

# Convert to DataFrame
mean_tumor_volume_df=pd.DataFrame(mean_tumor_volume)

# print(mean_tumor_volume_df.head())

mean_tumor_volume_df=mean_tumor_volume_df.reset_index()

print(mean_tumor_volume_df.keys())

# Preview DataFrame
mean_tumor_volume_df.head()


# In[3]:


# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
stem_tumor_volume=drug_timepoint_group['Tumor Volume (mm3)'].sem()

# Convert to DataFrame
stem_tumor_volume_df=pd.DataFrame(stem_tumor_volume)
stem_tumor_volume_df=stem_tumor_volume_df.reset_index()

# Preview DataFrame
print(stem_tumor_volume_df.keys())
stem_tumor_volume_df.head()


# In[4]:


# Minor Data Munging to Re-Format the Data Frames
mean_tumor_volume_df_pivot=mean_tumor_volume_df.pivot(index='Timepoint',columns='Drug',values='Tumor Volume (mm3)')
stem_tumor_volume_df_pivot=stem_tumor_volume_df.pivot(index='Timepoint',columns='Drug',values='Tumor Volume (mm3)')

# Preview that Reformatting worked
mean_tumor_volume_df_pivot


# In[5]:


# Standard Error of Tumor Volumes Grouped by Drug and Timepoint
stem_tumor_volume_df_pivot=stem_tumor_volume_df.pivot(index='Timepoint',columns='Drug',values='Tumor Volume (mm3)')
stem_tumor_volume_df_pivot


# In[6]:


mean_tumor_volume_df_pivot.keys()


# In[7]:


stem_tumor_volume_df_pivot.index


# In[38]:


# Generate the Plot (with Error Bars)
fig, ax=plt.subplots()
mtv_df=mean_tumor_volume_df_pivot
stv_df=stem_tumor_volume_df_pivot

mtv_timepoint=mtv_df.index

i=0
for drug in drug_list:
    ax.errorbar(mtv_timepoint, mtv_df[drug], yerr=stv_df[drug], marker=markers[i], color=colors[i])
    i+=1
    
plt.legend(drug_list,loc="best")

i=0
for drug in drug_list:
    plt.plot(mtv_timepoint, mtv_df[drug], color=colors[i])
    i+=1

plt.title("Tumor Response to Treatment")
plt.xlabel("Timepoint (Days)")
plt.ylabel("Tumor Volume (mm3)")
plt.grid()

# Save the Figure
plt.savefig('Tumor_Response_to_Treatment.png', dpi=300, format='png', bbox_inches='tight')
plt.show()


# In[36]:


# Show the Figure
plt.show()


# ![Tumor Response to Treatment](../Images/treatment.png)

# ## Metastatic Response to Treatment

# In[11]:


# Store the Mean Met. Site Data Grouped by Drug and Timepoint 
mean_met_sites=drug_timepoint_group['Metastatic Sites'].mean()

# Convert to DataFrame
mean_met_sites_df=pd.DataFrame(mean_met_sites)
mean_met_sites_df=mean_met_sites_df.reset_index()

# Preview DataFrame
mean_met_sites_df.head()


# In[12]:


# Store the Standard Error associated with Met. Sites Grouped by Drug and Timepoint
sem_met_sites=drug_timepoint_group['Metastatic Sites'].sem()

# Convert to DataFrame
sem_met_sites_df=pd.DataFrame(sem_met_sites)
sem_met_sites_df=sem_met_sites_df.reset_index()

# Preview DataFrame
sem_met_sites_df.head()


# In[14]:


# Minor Data Munging
mean_met_sites_df_pivot=mean_met_sites_df.pivot(index='Timepoint',columns='Drug',values='Metastatic Sites')

# Preview that Reformatting worked
mean_met_sites_df_pivot


# In[15]:


mean_met_sites_df_pivot.keys()


# In[16]:


# Reformatting Standard Error associated with Met. Sites Grouped by Drug and Timepoint
sem_met_sites_df_pivot=sem_met_sites_df.pivot(index='Timepoint',columns='Drug',values='Metastatic Sites')
sem_met_sites_df_pivot


# In[17]:


mean_met_sites_df_pivot.index


# In[39]:


# Generate the Plot (with Error Bars)
fig, ax=plt.subplots()
mms_df=mean_met_sites_df_pivot
sms_df=sem_met_sites_df_pivot

mms_timepoint=mms_df.index

i=0
for drug in drug_list:
    ax.errorbar(mms_timepoint, mms_df[drug], yerr=sms_df[drug], marker=markers[i], color=colors[i])
    i+=1

plt.legend(drug_list,loc="best")

i=0
for drug in drug_list:
    plt.plot(mms_timepoint, mms_df[drug], color=colors[i])
    i+=1

plt.grid()
plt.title("Metastatic Spread During Treatment")
plt.xlabel("Treatment Duration Days")
plt.ylabel("Metastatic Sites")
# Save the Figure
plt.savefig('Metastatic_Spread_During_Treatment.png', dpi=300, format='png', bbox_inches='tight')
# Show the Figure
plt.show()


# ![Metastatic Spread During Treatment](../Images/spread.png)

# ## Survival Rates

# In[19]:


# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
mice_cnt=drug_timepoint_group['Mouse ID'].count()
mice_cnt

# Convert to DataFrame
mice_cnt_df=pd.DataFrame(mice_cnt)
mice_cnt_df=mice_cnt_df.reset_index()

# Preview DataFrame
mice_cnt_df.head()


# In[20]:


# Minor Data Munging to Re-Format the Data Frames
mice_cnt_df_pivot=mice_cnt_df.pivot(index='Timepoint',columns='Drug',values='Mouse ID')

# Preview the Data Frame
mice_cnt_df_pivot


# In[40]:


# Generate the Plot (Accounting for percentages)

mice_cnt_timepoint=mice_cnt_df_pivot.index
i=0
for drug in drug_list:
    plt.plot(mice_cnt_timepoint, (mice_cnt_df_pivot[drug]/mice_cnt_df_pivot[drug].max()*100), marker=markers[i], linestyle='--', color=colors[i])
    i+=1
    
plt.grid()
plt.legend(drug_list,loc="best")
plt.title("Survival During Treatment")
plt.xlabel("Timepoint (Days)")
plt.ylabel("Survival Rate %")
# Save the Figure
plt.savefig('Survival_During_Treatment.png', dpi=300, format='png', bbox_inches='tight')
# Show the Figure
plt.show()


# ![Metastatic Spread During Treatment](../Images/survival.png)

# ## Summary Bar Graph

# In[23]:


# Calculate the percent changes for each drug
# Display the data to confirm

print(mtv_df.index)
perc_change=(mtv_df.loc[45,drug_list]-mtv_df.loc[0,drug_list])/mtv_df.loc[0,drug_list]*100
print(perc_change)
perc_change_tuple=tuple(perc_change)
perc_change_tuple


# In[24]:


drug_tuple=tuple(drug_list)
print(drug_tuple)
objects = (drug_tuple)
y_pos = np.arange(len(objects))
print(y_pos)
performance = perc_change_tuple
print(performance)
plt.ylim(min(perc_change_tuple)-10,max(perc_change_tuple)+10)
for drug in range(len(drug_list)):
    if performance[drug] > 0:
        growth=plt.bar(y_pos[drug], performance[drug], color='r', align='edge', alpha=0.8, width=1)
    else:
        reduction=plt.bar(y_pos[drug], performance[drug], color='g', align='edge', alpha=1, width=1)
    plt.text(y_pos[drug]+0.7, performance[drug], '%d' % int(performance[drug])+'%', ha='center', va='bottom', color='black')

plt.grid()
plt.axhline(y=0, color = 'black', linestyle='--')
plt.xticks(y_pos+1, objects)
plt.ylabel('% Tumor Volume Change')
plt.title('% Tumor Change Over 45 day Treatment')
plt.legend((growth, reduction), ('Tumor Growth', 'Tumor Reduction'), loc="upper left")
plt.savefig('tumor_chg_over_45.png', dpi=300, format='png', bbox_inches='tight')
plt.show()

