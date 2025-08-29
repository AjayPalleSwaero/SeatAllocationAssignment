#!/usr/bin/env python
# coding: utf-8

# In[85]:


import pandas as pd


# In[86]:


students = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Desktop\Shireesha_Projects\SSL\SeatAllocationAssignment\tsb01-dashboard-update\data\students.csv")
preferences = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Desktop\Shireesha_Projects\SSL\SeatAllocationAssignment\tsb01-dashboard-update\data\preference.csv")
seats = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Desktop\Shireesha_Projects\SSL\SeatAllocationAssignment\tsb01-dashboard-update\data\seat.csv")


# In[87]:


# Assuming your dataframe is named df
seats_melt_df = pd.melt(
    seats,
    id_vars=['CollegeID', 'Institution', 'TOTAL No. of seats',
             'TOTAL No. of students admitted',
             'No. of students joined in Orphan Quota',
             'No. of students Joined in PHC Quota'],
    value_vars=['SC', 'SC-CC', 'ST', 'BC', 'Minority', 'OC'],
    var_name='Category',
    value_name='Students'
)

#print(seats_melt_df.head())


# In[88]:


seats_melt_df = seats_melt_df.sort_values(by = ['CollegeID'])


# In[89]:


seats_melt_df[seats_melt_df['CollegeID'] == 147]


# In[90]:


#students.head(2)


# In[91]:


#preferences.head(2)


# In[92]:


student_pref_df = pd.merge(students, preferences, on = ['UniqueID']).sort_values(by=['Rank', 'PrefNumber'])


# In[93]:


#student_pref_df.sample(1)


# In[94]:


#student_pref_df.query('UniqueID == 1231127852')


# In[95]:


#student_pref_df.shape


# In[96]:


#seats_melt_df


# In[97]:


#student_pref_df.drop_duplicates(subset=['UniqueID', 'CollegeID', 'PrefNumber']).shape


# In[98]:


seats_melt_df['Category'].unique()


# In[99]:


student_pref_df['Caste'].unique()


# In[100]:


student_pref_df.columns


# In[101]:


#student_pref_df


# In[102]:


"""test_df = pd.DataFrame([{
    "UniqueID": 100, 
    "Name": "ROCKY", 
    "Gender": "Male",
    "Caste": "SC",
    "Rank": 1922,                
    "CollegeID": 244,
    "PrefNumber": 1       
}])

print(test_df)
"""


# In[103]:


#student_pref_df = pd.concat([test_df, student_pref_df])


# In[104]:


#student_pref_df


# In[113]:


unique_students = student_pref_df['UniqueID'].unique()
seat_df_copy = seats_melt_df.copy()

stu_dfs = []
for uni_id in unique_students:
    
    filter_df = student_pref_df[student_pref_df['UniqueID'] == uni_id]

    for index, row in filter_df.iterrows():
        
        is_allocated = False
        
        seat_exists_df = seat_df_copy[
            (seat_df_copy['CollegeID'] == row['CollegeID']) &
            (seat_df_copy['Category'] == row['Caste'])
        ]
        
        # ✅ only check seats if a row exists
        if not seat_exists_df.empty and seat_exists_df['Students'].values[0] > 0:
            
            # take one seat and minus that seat from seat_df_copy and allocate student that seat 
            student_rec_df = pd.DataFrame([{
                "UniqueID": uni_id, 
                "Name": row['Name'], 
                "Gender": row['Gender'],
                "Caste": row['Caste'],
                "Rank": row['Rank'],                
                "CollegeID": seat_exists_df['CollegeID'].values[0],
                "Institution": seat_exists_df["Institution"].values[0],
                "PrefNumber": row['PrefNumber']       
            }])    
            
            stu_dfs.append(student_rec_df)
            is_allocated = True
            
            # reduce 1 seat for that category in that college
            seat_df_copy.loc[
                (seat_df_copy["CollegeID"] == row['CollegeID']) &
                (seat_df_copy["Category"] == row['Caste']),
                "Students"
            ] -= 1
            
            break   # stop after allocation
        
        # if not allocated, create an empty allocation
        if not is_allocated:
            student_rec_df = pd.DataFrame([{
                "UniqueID": uni_id, 
                "Name": row['Name'], 
                "Gender": row['Gender'],
                "Caste": row['Caste'],
                "Rank": row['Rank'],                
                "CollegeID": " ",
                "Institution": " ",
                "PrefNumber": " "       
            }])    
            stu_dfs.append(student_rec_df)


# In[115]:


# Final allocation DataFrame
allocation_df = pd.concat(stu_dfs, ignore_index=True)
 
# Save results to CSV
allocation_df.to_csv(r"C:\Users\Lenovo\OneDrive\Desktop\Shireesha_Projects\final_allocation.csv", index=False)


# In[116]:


#seats_melt_df[seats_melt_df.CollegeID == 147]


# In[117]:


#seat_df_copy[seat_df_copy.CollegeID == 147]


# In[118]:


#filter_df


# In[119]:


#seats.columns


# In[120]:


#seats_melt_df.columns

